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


## 20. vFHE V11 — systematic-only native extractors lose coded distance amplification (2026-10-14)

**One primary hypothesis and one cheapest decisive falsifier:**
Assume, generously, that EACH native CRT field has an IDEAL sound extractor giving a legal bounded integer digit message and its *exact* valid field-linear RAA codeword. Suppose one extra common integer CRT-lift Merkle commitment binds the field projections, and a verifier authenticates/range-checks only t<m SYSTEMATIC columns (rather than encoded parity leaves), before inferring that all native extractors obtained ONE common bounded integer witness. Can this systematic-only sampling leverage the V9 good full-code distance to obtain small global error?

**RESULT: FAIL.** Even perfect independent field extractors, full Merkle authentication, and full native field-codeword validity DO NOT imply common scalar witness. With two bounded digit vectors differing in a SINGLE digit position, precisely ONE of the m systematic CRT-lift leaves violates the canonical digit range. Uniform postcommit t-subset systematic-only range checks miss it with **exact probability 1−t/m**. This is not a sound 128-bit proof for any t<m at m1024. It is a restricted critique of the PROPOSED auxiliary extraction approach, not a published vFHE attack, and is distinct from V10's sampling of the whole length-3m encoded word.

### Source vs model distinction [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025 ePrint2025/286, original Appendix F.2 physical pp50–51, cached mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest edition VERSION_UNVERIFIED. F.2 is a NATIVE FIELD-LINEAR matrix / Merkle proof, with verifier random r∈F^m and postcommit column openings Q checking Enc(rU_f)|Q=rUhat_f[:,Q]. It does not claim a common integer witness or the systematic-only integer range-check optimization. We posit IDEAL per-field extraction as an artificially **strong assumption**, not a proven consequence of published F.2. The ideal extractors are conceptual for a soundness reduction; if verifier literally learns ALL extracted witness digits, it can simply compare them, so that situation is not the tested private-commitment protocol.

### General exact theorem [DERIVED]

Let p,q>β−1 be distinct CRT primes and G_Z=[I_m | P_Z] any systematic integer encoder (RAA or otherwise). Let A_β={0,…,β−1}^m. Suppose two bounded legal vectors a,b∈A_β are extracted fieldwise, their full field codewords match one SAME integer CRT-leaf array Y coordinatewise,

    Y mod p = Enc_p(a),    Y mod q = Enc_q(b),

and a_j=b_j for all j≠j*. If a_(j*)≠b_(j*) then, at the first m systematic leaves, the unique canonical CRT lift Y_j∈[0,pq) satisfies

    Y_j∈[0,β−1] iff a_j=b_j.

Proof: if Y_j<β<min(p,q), then reducing modulo p and q gives the SAME integer, forcing a_j=b_j; if equal, canonical CRT lifting returns their common small integer. Consequently the systematically out-of-range set is EXACTLY {j*}, although the remaining parity codeword positions may differ in Ω(m) coordinates for good G.

For the root fixed before uniformly selecting Q_sys⊂[m] of size t without replacement and range-checking ONLY j∈Q_sys,

    Pr[accept | a≠b one digit] = Pr[j*∉Q_sys]
                             = C(m−1,t)/C(m,t)
                             = 1−t/m.

More generally, for any FIXED sampling distribution independent of the hidden differing index and touching at most t distinct systematic coordinates, sum_j Pr[j checked]≤t, so some index j* has Pr[j* checked]≤t/m; a prover able to choose this mismatch before sampling achieves acceptance probability ≥1−t/m. This last minimax argument does NOT claim to cover arbitrary root-dependent inspection algorithms; the exact uniform postcommit formula does.

At illustrative m1024,t128, acceptance probability=0.875; t1023 leaves ≥1/1024≈2^-10. Under uniform one-shot without-replacement systematic-only range sampling, ensuring <2^-128 for a one-digit mismatch requires t=m (unless some additional independent cross-domain check is used).

**Positive exact sufficiency boundary:** If EVERY one of the m systematic canonical CRT leaves is proven in the common digit interval [0,β−1], AND both per-field exact bounded-digit codeword extraction premises hold, then every extracted a_j=b_j=Y_j. Thus complete systematic range enforcement WOULD prove common witness equality. That is a **different, stronger design** (m checks or a sound ZK range proof); may reveal low-entropy private digits if openings are public. The negative result rules out expecting coding-distance amplification from only a small SYSTEMATIC sample, not every approach to cross-field binding.

### Exact one-root binary toy [EXPERIMENT]

Take m=8, β=2, true unweighted repeat-2, independently seeded perm1/perm2, two positive prefix accumulators, seed20261014, G∈Z^{8×24}. Select a=0 and b=e6, differing ONLY in systematic position j*=6. Both are valid Boolean messages; their full field-linear codewords are EXACT and different. Use source-form 49-bit p=281474976829441 and q=353581838970881, each congruent 4097 mod 8192 for source ring N8192,d4; both >honest integer H=m(2m+1)(β−1)=136.

Construct each integer CRT leaf

    Y_j = Enc_Z(a)_j + p·(((Enc_Z(b)_j−Enc_Z(a)_j)·p^(−1)) mod q),

using unique representative 0≤Y_j<pq. The ONE SHA256 Merkle root is

    7052562f3d88036af8dde743bc064029436bd089f2f71546ffa64741ea9bf7f3.

ALL 24 authentication paths verify, modification fails, and both fields satisfy their exact native codeword relation at EVERY coordinate (including arbitrary scalar multiples). Only systematic leaf 6 violates [0,β−1]. By contrast, the FULL encoded codeword differences lie at 17 of 24 coordinates (the systematic position 6 plus every parity position 8..23); 17 leaves violate the full honest canonical range [0,H]. This shows explicitly WHY systematic-only checking throws away V9's coding distance amplification.

EXACT exhaustive all sampled systematic subsets:
- m8,t1: accept 7/8=87.5%;
- t2:21/28=75%;
- t4:35/70=50%;
- t6:7/28=25%;
- t7:1/8=12.5%;
- t8:0/1=0.

This is exact, not a random Monte Carlo measurement. Source-style m1024,t128 acceptance=87.5% follows from the general formula, NOT from a performed m1024 F.2 experiment.

Local independently reproducible STD-LIB Python (not GitHub file):
`/mnt/data/vfhe_v11_systematic_extraction_gate.py`
SHA256 `6a2275f3305d23071bc62724b31058997c18928a356b56cda7c49411e01f9a17`.
JSON `/mnt/data/vfhe_v11_systematic_extraction_gate_results.json`
SHA256 `cc285ae1a6f7fd1b00138ab559161fcfaccfb6be8dd3cb6fb5fbe508748d94ee`.
Script executes with zero external libs, rebuilds both interleavers + full matrix, CRT leaf array, one Merkle root and every opening, checks field linearity, and enumerates all systematic t-subsets.

### End of V11 / decision

**FAIL:** \"Independent field-native bounded-digit exact-codeword extraction plus a shared CRT-leaf Merkle root and a FEW SYSTEMATIC-only range checks imply a single globally extracted bounded integer witness with strong soundness.\" The exact one-digit mismatch remains undetected with Pr=1−t/m. Neither a hash collision nor a field-codeword validity flaw is needed.

**KEEP / important protocol separation:**
(1) Complete systematic position range proof would imply equality, but may leak witness / cost m.
(2) Parity-encoded column checks CAN harness the V9 bounded-digit full code distance and V10's conditional exponential query bound **IF** every field codeword is already soundly extractable into a legal bounded digit vector and sampled shared integers are range checked. Proving that extraction is a major distinct soundness step. The current original F.2 verifier samples arbitrary native r and q1 vectors, and V9's restricted distance alone cannot prove this prerequisite.
(3) A ZK-friendly succinct proof of a single committed integer vector plus all range and cross-field reduction relations could potentially solve equality directly, but its cost/security/protocol fit is UNKNOWN. Do not call this a finished contribution.

**V12 next test (PI continuation only):** Stop toy one-root sampling variants. Assess ONE concrete *noncircular and zero-knowledge-compatible* primitive for jointly proving the relation R_diag: there exists a single bounded integer vector a with native component vectors equal to a mod all p_i, WITHOUT disclosing digit values. First cheapest falsifier: whether using a field-native Pedersen/vector commitment with a single arithmetic-field commitment can claim binding simultaneously into different CRT characteristic fields **without explicit cross-field encoding/reduction proof**. If not, KILL that shortcut and identify minimal enforceable constraint. Do not implement full PCS until these statements are precise.

**Status: FAIL naive systematic-only extraction gate, PASS exact minimax probability/one-root counterexample. STATE_UPDATE=YES independent vFHE V11; global I192 unchanged. Novelty unverified, no attack on original protocol.


## 21. vFHE V12 — commitment equality across CRT fields requires explicit knowledge-sound linking and injective canonical integer range (2026-10-14)

**Exactly one primary hypothesis:** Having ONE hiding vector commitment C over a third, unrelated prime-order message group (or a third arithmetic prime field) and having independently valid native CRT-field bounded-digit/range proofs is ALREADY enough, by the binding property of C alone, to ensure all native field digit values denote one shared integer witness, WITHOUT an explicit cross-domain linking/encoding-and-range proof.

**Result:** **FAIL the shortcut**, with two independently checkable logic/arithmetic countercases. **PASS a strictly CONDITIONAL sufficient linking relation** with a proof by contradiction from commitment binding; does NOT construct or benchmark a cross-field ZK/knowledge-sound protocol. **Novelty: existing commit-and-prove/modular equality and range proof techniques are direct prior art, so the logic statement itself is not new.**

### Grounded primary original proof interface [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, Appendix F.2 physical pp50–51, Research MCP cached GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official parity VERSION_UNVERIFIED. F.2 commits individual native FIELD-coded rows as Merkle columns, checks arbitrary r·U_f and q_1·U_f relations, **not** shared canonical bounded-integer commitment openings across distinct characteristics. Proposed C and auxiliary link proofs in V12 are NOT part of the source system.

### Failed shortcut #1: unlinked commitment [DERIVED]

Take distinct native primes p1,p2>β, digit domain D=[0,β−1], β=9. Let native extracted valid digit values be a1=1 in Fp1 and a2=8 in Fp2. Both satisfy all their **independent** digit range and native codeword consistency relations. Choose an arbitrary separately valid hiding commitment C to 1 in a third group/message field whose scalar order r>β. If neither native proof has any predicate linking the extracted a_i to the message OPENING of C, the conjunction

    Exists a1,a2: nativeValid_p1(a1) ∧ nativeValid_p2(a2) ∧ CommitWellFormed(C)

does NOT imply a1=a2, even assuming perfect binding of C. Counterexample has no hash collision or cryptographic failure. Replacing CommitWellFormed with an actually KNOWLEDGE-SOUND opening/equality relation is necessary.

### Failed shortcut #2: modulus alias even when native values are "opened" into ONE group commitment [DERIVED]

Let a commitment have cyclic scalar message group order r. For any blinding rho, the algebraic Pedersen expression is

    Com_r(a;rho)=g^a h^rho = Com_r(a+r;rho).

Take β=9, r=7 and legal digit values 1 and 8 (<β). Both native fields p1,p2>β can separately prove/know openings (1,rho) and (8,rho) for SAME C, with the exact SAME blinding, without discrete-log attack. But a1≠a2 over integers. Thus even a value-link that proves equality MOD r (not a canonical range-injective encoding) does not necessarily prove equality in Z.

**Important practical scope:** Modern prime-order commitment group may have r≈2^255 and source digits β≈2^20, so this toy r<β collision is NOT applicable once β≤r is explicitly established. In the toy group h=g^3 and discrete logs are knowingly trivial; the experiment is ONLY a reproducible modular-identity test, NOT a secure instantiation or a cryptographic soundness claim. The alias identity holds algebraically in EVERY order-r group regardless of the discrete log relationship. Scalar vector/group commitments may require additional coordinate-binding assumptions and safe encodings.

### Conditional sufficiency theorem: the actual noncircular statement to prove [DERIVED]

Let D=[0,β−1] with β≤r and β≤min_i p_i. Let Com_r be a computationally MESSAGE-BINDING commitment to a canonical integer vector in D^m via an injective vector encoding into the commitment message space; *not* merely a same-looking public group element. Suppose every native CRT proof is simultaneously (i) knowledge sound for a native field digit vector u_i∈F_(p_i^d)^m and (ii) knowledge sound for the **link** that C opens to the corresponding canonical integer vector a_i∈D^m satisfying

    C = Com_r(a_i;rho_i),
    u_{i,j} = embed_F_(p_i^d)(a_{i,j}) for ALL j.

Binding says if a_i≠a_l, the collected valid proofs/extracted witnesses would induce two openings of the SAME C to two different canonical messages, violating computational binding. Thus except with binding/knowledge-soundness errors, ALL a_i=a*, and their native field digit vectors are reductions/embeddings of the SAME bounded integer a*.

For EACH digit in [0,2^k) with 2^k≤min(r,p_i), the integer can be expressed as k canonical Boolean bits

    a_j=Σ_{b=0}^{k−1} 2^b v_{j,b},   v_{j,b}∈{0,1}.

When a_j< p_i, this integer equals its image in F_(p_i) AND extension F_(p_i^d); for THIS digit-equality constraint no quotient/carry gadget for reduction mod p_i is logically necessary. HOWEVER proving in ZK that EACH native committed field value u_{i,j} equals that SAME canonical digit (or bit decomposition) is absolutely necessary. A separate SNARK/CP-SNARK proof tied to C could enforce this; none is provided or verified here. If β is not a power of two, add explicit a_j<β rather than only k-bitness. For packed vector encodings avoid alias from carries / group-order reductions; safest statement is a sound vector commitment with explicitly proven coordinate messages.

There is **no unital ring homomorphism** F_p→F_q for different primes p≠q: if a unital hom existed, mapping p·1=0 would force p·1=0 in F_q, impossible when q≠p. Common INTEGER canonicalization, not a field homomorphism, is the correct interface.

**This theorem is purely compositional conditional cryptographic reasoning; it is NOT proof of a specific commitment's DL binding/PCS knowledge extraction/ZK or error accounting.** If field-native proofs merely reference C as unused public input, shortcut #1 returns. If group order insufficient or packing noninjective, shortcut #2 returns.

### Exact minimal executable gate [EXPERIMENT]

Local Python: `/mnt/data/vfhe_v12_cross_field_binding_gate.py`; SHA256 `3f8127d432f737c475a23463dd70a796fd8bd68fc4df11eba26d06c1fbfd4ed7`.
JSON: `/mnt/data/vfhe_v12_cross_field_binding_gate_results.json`; SHA256 `5e7b0db8e5693dff82f2e2c81dd59d4a7ed5e6f06abca2c8b9822834517268db`.
Files LOCAL ONLY; not GitHub repository bytes.

Native p1=281474976829441, p2=353581838970881 are previously verified source-form 49-bit CRT primes N8192,d4. Toy β=9, a=1, b=8. (1) Shared C over toy r=101 message subgroup, valid independent bounded native digit statements both TRUE but NO link, so a≠b. (2) In order-7 subgroup of F_29^*, with g=16, h=g^3, rho=4, exact Pedersen-form modular evaluation satisfies Com(1;rho)=Com(8;rho); both native values legal; there is NO single integer in D mapping to 1 and 8 in their native large prime fields. Group toy is intentionally INSECURE, only demonstrates algebraic modular alias. (3) When r=101≥β=9, brute enumeration of all 9 canonical digits proves unique integer representation modulo r; with the SAME knowledge-sound commitment-link openings and range, equality can be inferred, conditional on actual commitment binding. Bit reconstruction for both digit values checked exactly. The tests are symbolic/algebraic only: NO actual NIZK, Pedersen security reduction, field-native PC test, or performance results.

### Close prior art and novelty gate [FACT, external]

Benarroch, Campanelli, Fiore, Gurkan, Kolonelos, *Zero-knowledge proofs for set membership: efficient, succinct, modular*, Designs, Codes and Cryptography 91 (2023), DOI https://doi.org/10.1007/s10623-023-01245-1, Sections 4.2.8 (modEq) and 4.3 (range), directly formalizes ZK **same value modulo group order between commitment types** and uses INTEGER range constraints to exclude modular collision ambiguities. Its commit-and-prove composition mechanism also explicitly links independently proven predicates on one committed hidden value. This is genuine PRE-EXISTING technology; V12's observation must NOT be presented as novelty or named a completed cross-field vFHE bridge. Assess whether specific source-native PCS context admits a lower-cost special-purpose link; no such advantage tested yet.

### Research decision and V13 gate

**KILL:** "Use just ONE third-field commitment with independent CRT-native lookup/PCS proofs; commitment's binding automatically forces diagonal common witness" (no link).
**KILL:** "Same linked commitment openings imply SAME integers" absent canonical injective range constraints when β>r or vector packing wraps modulo r.
**KEEP, CONDITIONAL:** One shared canonical bounded integer vector/bit commitment; provably binding and ZK; each native CRT-field witness/extracted codeword linked KNOWLEDGE-SOUNDLY to its corresponding canonical coordinate/bit decomposition, with β≤min_i p_i and injective commitment encoding β≤r; proof errors budgeted.

**Next V13 if PI continues:** ONE cheapest **amortized/batched cross-domain LINK proof** test: can we replace m·μ individual scalar links by a common random linear-combination check while preserving extraction and commit-before-challenge soundness over different CRT primes? Demand explicit false-witness soundness probability, no-wrap or proof-system-link to committed vector, and per-field computational cost. Do NOT yet claim repair, privacy, or fast PCS.

**End V12:** STATUS=FAIL automatic cross-characteristic commitment binding; PASS exact necessary-modEq+range+link conditions and toy verification; NOVELTY NOT VERIFIED; STATE_UPDATE=YES independent vFHE V-series only, global general FHE I192 remains frozen.


## 22. vFHE V13 — 128-bit integer challenge collapses to ≈48-bit base-field batch-link soundness (2026-10-14)

**ONE PRIMARY HYPOTHESIS / DECISIVE TEST.** A proposed cheap *single random linear-combination link* can amortize m·μ individual hidden digit equalities by choosing a GLOBAL 128-bit integer Fiat–Shamir scalar alpha, reducing alpha modulo each ~49-bit CRT prime p_i (then embedding in the native extension field F_(p_i^d)), and checking in each native field

    ∑_(j=0)^(m−1) alpha^j (u_(i,j) − a_j) = 0.

Claim to FALSIFY: This ONE batched relation enjoys 128-bit false-witness soundness simply because the source common integer challenge has 128 bits or because the native proof arithmetic uses F_(p_i^4). We grant an IDEAL cross-field batch equality oracle binding the committed a and extracted native u_i; this is a STRONGER assumption than any implemented protocol, making the falsifier robust.

**STATUS: FAIL the 128-bit one-shot shortcut**; exact lower bound ~2^−48 per inconsistent CRT component for a legal TWO-COORDINATE Boolean difference. PASS conditional math improvement when using a TRUE full-extension random challenge or repeating independent prime-field checks, but neither produces an actual zero-knowledge link to a third-field shared commitment. Novelty NOT VERIFIED; random batching/Schwartz–Zippel and characteristic-domain conversion are standard principles.

### Primary source anchors [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286 https://eprint.iacr.org/2025/286, Research MCP inspected mirror (52pp, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, version-unverified):
- §3.1 physical p10 specifies native CRT primes p=1+(2N/d)a, a odd, native fields F_(p^d) for d configurable.
- Appendix F.2 physical p50–51 uses randomized field-linear checks and Merkle commitments. It does NOT describe our proposed global 128-bit cross-CRT integer challenge or third-field canonical Pedersen commitment.
Existing literature on random linear-combination batching and polynomial identity testing is background, not this candidate's novelty (e.g. 2024+ literature on batched polynomial evaluations, and Schwartz–Zippel).

### Exact two-digit counterexample [DERIVED, no cryptographic assumptions]

Set β=2, input code/message length m≥2. In the canonical committed integer digit vector use

    a=(0,1,0,…,0),

while ONE native CRT field's extracted/legal Boolean digit vector is

    u=(1,0,0,…,0).

Both satisfy [0,β−1]^m, but u≠a. Their discrepancy d=u−a=(1,−1,0,…,0) has constant coefficients in EVERY prime-field and extension-field incarnation.

The batched polynomial is

    F_i(alpha)=∑_j alpha^j (u_j−a_j)=1−alpha ∈ F_(p_i)[alpha].

It is not the zero polynomial, but **passes** iff alpha≡1 mod p_i.

If alpha is uniform in F_(p_i), exact false acceptance is 1/p_i. If alpha is uniform among 128-bit NONNEGATIVE integers 0≤alpha<2^128 and embedded as alpha→(alpha mod p_i)·1 in F_(p_i^4), acceptance probability is EXACTLY

    [floor((2^128−2)/p_i)+1] / 2^128.

This is within 2^−128 of 1/p_i, since 2^128 distinct integers reduce almost uniformly to Fp_i. In particular: a 128-bit hash/random integer does NOT induce an F_(p_i^4)-uniform challenge via the **scalar integer embedding**; its image is contained entirely in the ~49-bit PRIME SUBFIELD. Degree-4 extension arithmetic alone provides no soundness amplification.

For genuine *independently, uniformly sampled* alpha∈F_(p_i^4), this particular nonzero degree-1 relation has **exact** acceptance probability 1/p_i^4, roughly 192 bit. But producing and proving a cross-field aggregate link for such alpha requires a separate protocol; an integer scalar α cannot be treated as uniformly distributed in the extension via simple reduction. Moreover a full uniform extension element requires much more entropy than just choosing a 128-bit integer; formal finite soundness depends on actual hash-to-field/challenge distribution.

For a general fixed error vector with polynomial F_i of degree≤m−1 over F_(p_i^d), standard Schwartz–Zippel gives Pr[pass]≤(m−1)/|F| for alpha uniformly in F. The displayed TWO-digit vector is a specific lower-bound witness showing one scalar prime-subfield test cannot guarantee 128 bits. Under a single FALSE CRT component and any number of honest other CRT components, full all-components verification still has this ~1/p_i false acceptance probability; requiring every component valid does not automatically multiply the error by the number of components.

### Exact source-form numeric check [EXPERIMENT]

Set source-form ring N=8192,d=4 (hence p=4096·odd+1), use the two previously verified 49-bit primes

    p1=281474976829441,
    p2=353581838970881.

Both pass deterministic Miller–Rabin suitable for 64-bit integers; p1≈2^48, p2≈2^48.329. The exact probabilities and effective bits from the formula are:

- p1: 3.552713677301223447e−15, approximately **48.000000 bits**.
- p2: 2.828199556036458081e−15, approximately **48.329038 bits**.

A single 128-bit global integer challenge mapped into these domains is insufficient for 128-bit proof soundness in THIS perfectly authenticated hypothetical aggregate-check model. For a single fixed invalid component, three INDEPENDENT prime-field samples yield around 144/145 bits for this degree-1 witness, if every sample is committed properly and proofs have independent errors; this is NOT a full protocol error bound. For general degree m−1 polynomial, a single base-field scalar random test may have failure upper bound ~m/p, which is even weaker than 1/p.

**Timing attack:** if alpha is announced before a/u are bound, cheating can choose a nonzero discrepancy in the alpha-weighted linear hyperplane and pass with probability 1. The postcommit challenge ordering is mandatory for even the 1/p analysis.

**Reproducible standalone exact gate:** `/mnt/data/vfhe_v13_prime_subfield_batching_gate.py`, SHA256 `7aa6a7e28c5f0f782db89b4e7540273cb9fbf0d77468d234018cdb3a15c0af65`; result JSON `/mnt/data/vfhe_v13_prime_subfield_batching_gate_results.json`, SHA256 `eb5a40bf1ebdd8f336a55e32175e372071ab3fc7fdddd45e5e3a6a03f76d79df`. The script generates exact probabilities, verifies both source-form primes' primality and congruences, enumerates F17/F29/F37 scalar roots (exactly alpha=1), and checks arithmetic of the malicious two-digit relation. These are LOCAL files and do not implement third-field Pedersen/PCS link proofs, privacy, SNARK or 128-bit multi-component error accounting.

### Scientific decision: avoid a false batching contribution

**KILL one-shot 128-bit claim:** Global 128-bit integer alpha reduced mod each CRT p_i (and injected into native F_(p_i^4)) creates at most base-field soundness; a two-coordinate false Boolean witness passes with probability approximately 2^−48. Extra CRT domains do not remove a discrepancy isolated to one domain.

**KEEP two conditional alternatives (NOT implementations):**
(A) At least several independent BASE-FIELD challenges per component, with errors for a general fixed discrepancy polynomial carefully bounded, all commitments fixed BEFORE challenges; challenge count depends on m, component count and 128bit target. For arbitrary d vector, a **FULL RANDOM VECTOR** of field coefficients has exact 1/p_i false acceptance rather than the possible (m−1)/p_i for one power-derived scalar challenge, though this still does not solve cross-characteristic commitment binding.
(B) Truly uniform extension-field challenge(s) α_i∈F_(p_i^4) can yield ≈196-bit challenge space and a native polynomial identity check error≤(m−1)/p_i^4. However proving the full-extension aggregate from an unrelated-prime hidden vector commitment requires a NEW knowledge-sound, zero-knowledge-compatible cross-field link; native F.2 arbitrary field coefficients cannot simply act on a third-field Pedersen exponent.

**V14 NEXT_ACTION (only on PI continuation):** One concrete sound cross-field aggregated **extension-field** relation candidate: Given common canonical bit/vector commitment C and a TRUE α_i∈F_(p_i^4), can a prover furnish a succinct proof that the native batched value z_i=Σ α_i^j u_i,j equals Σ α_i^j embed(a_j), while binding a to C, WITHOUT silently assuming an F_(p_i^4) scalar acts homomorphically on a DIFFERENT prime-order commitment group? First test the existence of an explicit matching relation at all 4 Fp_i basis components and assess unavoidable native-field multiplication/bit constraints. If a cheap sound link does not follow, mark UNCLEAR or recommend PI pivot to a known commit-and-prove implementation rather than inventing zero-cost linking.

**End V13:** STATUS=FAIL one-global-128bit-integer scalar batch link soundness; PASS exact two-coordinate legal falsifier and prime-subfield entropy analysis; OPEN cross-characteristic aggregate link/ZK/knowledge extraction/cost; STATE_UPDATE=YES independent vFHE only, global I192 unchanged.


## 23. vFHE V14 — quotient obstruction for extension-field batched links

Date: 2026-10-14. Separate V-series: V14; general FHE I192 remains frozen.

**Primary hypothesis:** A genuine postcommit F_(p^4) random challenge makes it possible to directly verify the extension-field aggregate against a third-field Pedersen/vector-commitment linear aggregate, without explicit modular reduction linking. **STATUS: FAIL shortcut; PASS exact quotient relation; full CP/PCS proof and cost UNCLEAR.**

**Source [FACT]:** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286, §3.1 (physical PDF p10) uses characteristic p and degree-d CRT fields; Appendix F.2 pp50–51 is a separate native-field Merkle/Brakedown construction. Neither the cross-field Pedersen bridge nor this batched scheme is part of the source paper. Inspected cached 52pp research-MCP mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; latest revision parity VERSION_UNVERIFIED.

**Proof [DERIVED]:** Fix a canonical digit vector a_j in [0,beta−1], integer commitment scalar modulus r, and native K=F_p[theta]/f(theta), deg f=4. Let alpha∈K be a TRUE extension element and expand its powers alpha^j=Σ_(t=0)^3 c_(j,t) theta^t. Lift c_(j,t) to canonical integers ctilde_(j,t) in [0,p−1]. Put S_t=Σ_j ctilde_(j,t)*a_j in Z. The native honestly computed aggregate z=Σ_j alpha^j embed(a_j) has coordinates z_t=S_t mod p. The CORRECT cross-characteristic relation therefore needs witnesses k_t with
    S_t=z_t+p*k_t, 0≤z_t<p, 0≤k_t≤floor(m*(p−1)*(beta−1)/p), t=0,1,2,3.
The zero-quotient shortcut S_t=z_t is not complete. A Pedersen homomorphic combination of separately committed digit scalars binds S_t mod r, NOT native z_t mod p; a single vector Pedersen commitment with independent generators does not itself admit arbitrary weighted-sum openings. Four base-coordinate relations MAY BE PACKAGED into one succinct proof; this is NOT a four-proof-size lower bound.

**One exact counterexample [EXPERIMENT]:** K=F_29[theta]/(theta^4+theta+5), irreducible polynomial verified, alpha=28+theta, m5, beta16, honest a=(2,3,5,7,11), unrelated scalar prime r=10007. Exact independent integer aggregates S=(562,423,253,282); native F_29^4 coefficient vector z=(11,17,21,21); quotient k=(19,14,8,9). Every S_t=z_t+29*k_t, all S_t<r yet all S_t differ from z_t. Thus raw group/native equality REJECTS an honest witness even though there is NO wrap modulo r. Even m2,a=(1,1),alpha=28+theta gives S=(29,1,0,0),z=(0,1,0,0),k=(1,0,0,0).

**Illustrative 49-bit envelope [DERIVED]:** p=281474976829441, m1024,beta=2^20. Per-basis lifted S_t≤m*(p−1)*(beta−1)=302231166800824369152000 (78 bits). Each k_t≤1073740799 (30 bits). Hence a normal ~255-bit commitment scalar would not wrap under these illustrative parameters, BUT field-p quotient constraints still matter. Message length m1024 is NOT asserted to be the paper's actual PCS row dimension.

**Reproduction:** Local /mnt/data/vfhe_v14_extension_field_link_gate.py SHA256 cf972c3fa8b95ad43075ed7859dea48bdd5b18b033805643a17702f81527da44; JSON /mnt/data/vfhe_v14_extension_field_link_results.json SHA256 1948173a26ffdffb415500541686450a1cfe688eecb27eaafa2e934b3e96b452. Executed exact extension polynomial arithmetic and integer quotient checks. Not a real Pedersen protocol, ZK proof, PCS extractor, random-ensemble experiment, security or performance benchmark.

**Prior art / novelty gate:** Modular equality, range and commit-and-prove techniques exist, e.g. Benarroch et al., *Zero-knowledge proofs for set membership: efficient, succinct, modular*, Designs Codes Cryptography (2023), DOI10.1007/s10623-023-01245-1, §4.2.8. Existing cross-field glue and non-native arithmetic can be expensive; V14 is an elementary completeness gate, not new cryptography.

**NEXT_ACTION V15 (PI continuation):** ONE minimal operation-count/feasibility gate: can a known linear-functional opening and quotient-based CP link amortize over m and CRT components versus per-digit links? Establish which arithmetic and group multi-exponentiation operations remain, without invented speedups. Full native F.2 extraction and zero-knowledge still OPEN.

End V14: STATUS=FAIL shortcut / PASS exact necessary arithmetic relation; STATE_UPDATE=YES in independent V-series only.


## 24. vFHE V15 — proof-communication savings do not remove weighted MSM work in naive cross-field batch links

Date 2026-10-14. Global FHE I192 remains frozen; V-series V15 only.

**One primary falsifiable hypothesis:** After V14 corrected the cross-characteristic aggregate by quotient witnesses, replacing mu*m per-digit cross-field links with d=4 batched aggregate links (a) via m individually homomorphic Pedersen digit commitments or (b) via one Pedersen vector commitment plus a standard IPA linear-functional opening ALSO gives essentially sublinear verifier group work O(mu*d*log m), not merely shorter proof communication. Test this in two explicitly named, unoptimized protocol interfaces; do NOT claim general cryptographic lower bounds for all possible batch proof systems.

**V15 STATUS: FAIL sublinear-group-work shortcut for these straightforward instantiations; PASS symbolic operation counts and an exact rank-4 extension algebra check; UNCLEAR net prover/verifier runtime, real proof byte size, advanced multilinear batch openings, and whole ZK/PCS design. NOT an established optimization or novelty.**

**Source / scope [FACT]:** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286, original §3.1 physical PDF p10: ring CRT R_(q0) factors for each prime p_i into k=N/d extension fields F_(p_i^d); Appendix F.2 pp50–51 Merkle Brakedown field-linear commitment and queried-column testing; F.3 pp51–52 RS code alternative. Cached 52-physical-page GitHub-mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, official latest version parity UNVERIFIED. Original paper DOES NOT implement our cross-characteristic canonical-digit commitment, IPA bridge, or the operation counts below.

**Relevant known technique [FACT]:** Halo2 Book `https://zcash.github.io/halo2/background/pc-ipa.html`: vector Pedersen polynomial commitment; modified inner-product knowledge argument for committed linear functional; O(log m) communication and log m recursive L/R rounds. Halo2 Book `https://zcash.github.io/halo2/background/recursion.html`: conventional IPA verifier has a length-m multi-exponentiation bottleneck, which recursion/accumulation can DEFER and amortize. Bulletproofs (Bünz et al., IEEE S&P 2018, ePrint 2017/1066) also uses log-size arguments but generally linear proving/verification work. These known asymptotics do not prove that a V14 cross-prime quotient relation is implementable in the same scalar field. A generic IPA proves mod-r inner products, not native mod-p equality.

**Exact arithmetic interface [DERIVED]:** Let F be the TOTAL count of field instances which are individually linked, not automatically the number mu of CRT primes; extension degree d=4. Native alpha in F_(p_i^4) generates d=4 base-field coefficient forms per field instance. The corrected relation for each t=0,...,3 is:
   S_(i,t)=sum_(j=0)^(m−1) ctilde_(i,j,t)*a_j;
   S_(i,t)=z_(i,t)+p_i*k_(i,t),
with a_j in canonical [0,beta−1], ctilde in [0,p_i−1], z in [0,p_i−1], k appropriately bounded.
There are exactly L=4F linear-form CLAIMS and 4F quotient witness variables in this separated model. The dense coefficient matrix has L*m=4Fm entries. This is a count of scalar coefficients/terms, NOT a universal lower bound on any optimized algorithm, not a lower bound on proof size, and not an assertion that every native CRT slot must have a separate proof.

**Implementation path A, separately homomorphic digit commitments:** Publicly establish m scalar group elements C_j=g^(a_j) h^(rho_j), with digit bitness/range separately proved. For each base-coordinate functional form form D_(i,t)=product_j C_j^(ctilde_(i,j,t)). Computing/verifying each D in the direct MSM interface consumes m scalar-base PAIRS, so L*m=4Fm MSM input terms plus additions (and potential batch-MSM speedups). Derived D commits to S_(i,t) modulo group scalar order r; the CP proof must establish S_(i,t)=z_(i,t)+p_i k_(i,t) with bounded integer lift and link native z to previously committed/extracted field value. Publishing D without recomputing or soundly proving derivation does not bind it to C_j. No complete such CP verifier implemented.

**Implementation path B, compact Pedersen vector commitment and standard independent IPA openings:** One group element C=product_j g_j^(a_j) h^rho (its construction still processes m inputs). Each one of 4F public arbitrary coefficient vectors needs an appropriate IPA linear-functional claim. The standard separate-openings baseline has about 2 log2(m) L/R group elements per functional (for m a power of 2), and conventional verifier's length-m MSM, resulting in approximately L*m MSM input terms in THIS baseline. At m1024, 2log2m=20, so separate IPA fold messages contribute approximately 80F group elements. This excludes other scalars, Fiat–Shamir transcript data, quotient constraints, native statements, joint vector range proof, any CP proof objects, and shared-opening optimizations. It is an illustrative upper workload for an unbatched IPA strategy, not a MINIMUM proof size or full bytes for our proposed protocol. A known batch/multipoint opening or recursive IPA may change this substantially.

**Exactly checked parameterized workload [EXPERIMENT/SYMBOLIC]:** Choose hypothetical link dimension m=1024, d=4, beta=2^20, N=8192, native p=281474976829441. Then max integer aggregate S_t=m(p−1)(beta−1)=302231166800824369152000 (78 bits), max k_t=1073740799 (30 bits), and a naïve bit-decomposition has m*20=20480 Boolean digits to constrain ONCE for the shared a, independent of F (unless proof systems duplicate them). For illustrative mu in {2,4,8}:
 - If ONLY ONE field instance per prime must be independently linked, F=mu: number L=4mu forms; MSM terms 4096mu (8192,16384,32768); separate-IPA L/R group points 80mu (160,320,640). One commitment C vs m commitments C_j.
 - If *every* one of original k=N/d=2048 extension factors PER prime independently requires a separate cross-characteristic link, F=2048mu, L=8192mu, MSM terms=8388608mu (mu=4 ⇒33554432), separate-IPA L/R group points=163840mu (mu=4 ⇒655360). This is a CONDITIONAL high-workload architecture, NOT the source paper's measured cost, nor proof that across-factor batching is impossible.
 - In all cases the 4F coefficient aggregates have at least L*m terms in an EXPLICIT DENSE matrix representation; special structured algorithms or batching over native factors may improve costs. Four native quotient relations per instance CAN be jointly proved in one proof object; not four separate proof objects as a lower bound.

**Independent exact four-basis check:** In toy K=F29[theta]/(theta^4+theta+5), take alpha=28+theta. Coordinate vectors of powers 1,alpha,alpha²,alpha³ span K as F29-vector space: their 4×4 coefficient matrix has rank EXACTLY 4 (verified by finite-field elimination). Thus for a generic degree-4 challenge the one extension relation indeed expands into FOUR independent base-field coordinate linear forms; treating it as one single Fp scalar exponent equality drops constraints. Verify separately V14's honest lifted S=(562,423,253,282), z=(11,17,21,21), k=(19,14,8,9). This supports the arithmetic model, not the asymptotic MSM lower bound.

**Reproducible local-only evidence:** /mnt/data/vfhe_v15_batch_link_cost_gate.py SHA256 82406ea2e47ba58b700cec73c0aa069608af24b951000f7a2208619148843855; /mnt/data/vfhe_v15_batch_link_cost_results.json SHA256 d74231e2ba9d84811a55ecbca5715a9c5e753bf4bcc2667969e8f3dcdea89859. Two executions produced the same output and hashes. Pure exact integer/finite-field algebra and operation COUNTS, NO group MSM timing, NO IPA implementation, NO ZK prover/verifier or SNARK benchmark.

**Research decision:** KILL the strong performance claim "4F IPA links imply O(F log m) verifier group work and an end-to-end vFHE speedup" for the two standard direct implementations. KEEP only a conditional communication-size opportunity: independent IPA rounds use O(F log m) fold group elements versus a NAIVE mF independent link proof family, but neither is a security-complete cross-characteristic quotient/range proof and public computation can remain O(Fm). It is not meaningful to compare this to original native RS PCS without m, number of relevant CRT extension slots, prover/verifier operations, concrete α distributions, transcript errors, and privacy constraints.

**NEXT V16 (PI continuation only):** ONE exact falsifier for additional batching across the k=N/d native extension factors sharing the SAME base prime p. Can a postcommit random Fp-linear combination of their 4k native quotient/equality residuals reduce group-based functional openings to O(1) per prime (rather than 4k), while preserving a concrete error bound (about 1/p per independent round), and what base-field arithmetic / native extraction is still required? If cannot prove a sound shared-integer binding interface even under ideal native extractors, return UNCLEAR and recommend human review. No more generic count tables without a new decisive mechanism.

**End V15:** STATUS=FAIL sublinear-verifier-work claim for A/B; PASS algebra/rank and exact operation-count model; UNCLEAR total efficiency / actual protocol. STATE_UPDATE=YES independent vFHE; global general counter I192 unchanged.


## 25. vFHE V16 — batch native extension-factor link residuals once per CRT prime

Date: 2026-10-14. Independent vFHE V16, general I192 FROZEN.

**ONE PRIMARY HYPOTHESIS:** Assuming one canonical bounded integer witness vector a is already knowledge-soundly bound to a THIRD-FIELD hiding commitment and all native field witnesses/results are independently bound BEFORE the fold challenge, can the d*k=4*(N/4)=N separate native-base coefficient-link statements for ALL k extension factors of ONE CRT prime be collapsed into ONE third-field/group linear-functional opening per challenge round, with a precise false-witness probability and a real reduction in GROUP-work relative to V15's separately proven forms?

**STATUS: PASS EXACT ALGEBRA and conditional MSM-term reduction; no complete CP-SNARK or ZK proof constructed; end-to-end performance UNCLEAR and a large field-arithmetic cost remains.** Probability 1/p PER independent random-vector round for any fixed nonzero residual; one-shot 49bit insufficient for 128-bit; 3 independent rounds give conditional ~142bit union bound for four source-style p>2^48. No per-factor O(1) complete proof claim without ideal-binding premises.

### Source anchors and scope [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, IACR ePrint 2025/286, §3.1 physical p10 gives k=N/d extension factors per CRT prime p_i, each F_(p_i^d). Appendix F.2 physical pp50–51 uses field-native Merkle/Brakedown matrix commitment and random field-linear checks; no cross-characteristic integer Pedersen/IPA batching is present in the source. Research MCP inspected 52pp cached GitHub mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; official latest version parity VERSION_UNVERIFIED.

Existing randomized constraint batching is prior art (Schwartz–Zippel/random linear combination); see e.g. Halo2 Book proving system/vanishing argument https://zcash.github.io/halo2/design/proving-system/vanishing.html and linear IOP treatment https://link.springer.com/article/10.1007/s00145-022-09424-4. Standard IPA short functional opening: https://zcash.github.io/halo2/background/pc-ipa.html. V16 is NOT a claim of novelty.

### Exact folding statement [DERIVED AND PROVED]

Fix ONE native prime p. Suppose its k extension factors provide L=d*k base-coordinate claims:

    z_l = sum_(j=0)^(m-1) c_(l,j)*a_j    in F_p,   l=0,...,L−1.

Here c_l ∈ F_p^m are derived from separately sampled genuine native extension challenges, the SAME canonical integer digit vector a∈[0,beta−1]^m applies to ALL these rows, and the native z_l and the field witness vectors were committed and knowledge-soundly bound BEFORE the fold randomness. This shared-a premise is a MODEL ASSUMPTION; it must be separately mapped and validated for any actual source ring polynomial/digit indexing. The hidden a is already knowledge-soundly bound by the third-prime-group commitment C. Merkle roots/native commitments and all alpha values are transcript-bound before lambda.

Pick vector lambda=(lambda_0,...,lambda_(L−1)) uniformly and independently from F_p^L AFTER the above commitments. Define public folded native coefficient and folded native value:

    cbar_j = sum_l lambda_l c_(l,j) mod p;
    zbar = sum_l lambda_l z_l mod p.

Then the entirety of the L congruences reduces to ONE congruence per lambda:

    <cbar,a> = zbar   mod p.

For fixed nonzero residual vector e_l=<c_l,a>−z_l∈F_p, dot(lambda,e) is uniform in F_p: choose any e_t≠0 and condition on every lambda_l except lambda_t; unique lambda_t makes dot zero. Hence false-acceptance EXACTLY 1/p, regardless of L and m. With s independently sampled fold vectors and unchanged, pre-bound residuals, probability p^−s.

**Strict prerequisite:** If the prover may choose or change even one original z_l, native u_l, or its meaning AFTER seeing lambda, the fixed-residual argument fails; native field proof/extraction must authenticate *every* original z_l and its relation to u, not merely the aggregated zbar. Similarly if common a is not soundly bound to C before lambda, the prover may adapt a. A prover-generated zbar not proved equal to the bound native linear combination is useless; a compact third-field functional proof without such native validation is not sound.

### Preserve V14 cross-characteristic quotient correctness [DERIVED]

All fold operations above MUST be in F_p, **before** converting to the commitment scalar field. Choose canonical 0≤ctildebar_j<p and 0≤ztildebar<p. Define

    Sbar=sum_j ctildebar_j*a_j ∈ Z,
    Sbar=ztildebar+p*kbar,
    0≤kbar≤floor[m(p−1)(beta−1)/p].

A correct cross-characteristic CP linking relation must prove the joint statement: the third-field commitment C binds THIS a; the group linear-functional opening binds Sbar mod r with injective/canonical integer range so group r > m(p−1)(beta−1); the native previously bound z_l fold to zbar; ztildebar is its canonical lift and kbar is bounded; equality Sbar=ztildebar+p*kbar holds. Group-scalar calculation is NOT automatically a field-Fp homomorphism. This gives ONE modular quotient instance per fold round, not L separate quotient instances.

### Operation count: conditional but decisive in V15 direct baseline

For m=1024,N=8192,d=4, k=2048, L=8192 PER PRIME and mu=4 primes, s=3 independent fold rounds:
- V15 separate direct linear-functional openings: L*m=8,388,608 MSM scalar-base input TERMS per prime; all four primes 33,554,432.
- V16 folded direct baseline: s*m=3,072 MSM terms per prime; all four primes 12,288. This is factor 8192/3=2730.666... fewer MSM input pairs in these explicit approaches, NOT a runtime speedup bound or cryptographic lower bound.
- Field coefficient folding by an UNOPTIMIZED DENSE implementation still costs s*L*m=25,165,824 Fp multiply/add terms per prime; four primes 100,663,296. The verifier must compute/verify this coefficient vector, or rely on a separately sound protocol that does it. Native z folds add sL scalar mul-adds and native exact-value extraction still costs something.
- Standard separate IPA L/R folding group elements for m1024 ~2log2(m)*L=163,840 per prime; folded s*20=60 per prime, excluding modEq/range/native proofs. Different aggregation, preprocessing, structured FFT/coding, and recursion may change counts.
- With source-like p=281474976829441, beta=2^20, the REDUCED folded coefficient's canonical lifts stay below p. Sbar≤m(p−1)(beta−1)=302231166800824369152000 (78 bits), kbar≤1073740799 (30 bits), independent of L. This is why one quotient per fold can be safely bounded; combining lifted coefficients without first reducing mod p would require a different quotient bound.

**CONCRETE SOUNDNESS ACCOUNTING:** For mu=4 and every p_i>2^48, s=3 full independent Fp-vector folds per prime give union upper bound sum_i p_i^(−3) <4*2^(−144)=2^(−142). This is ONLY the folding error, conditional on fixed native/code/committed integers, independent Fiat–Shamir challenges, no other soundness errors, and honest canonical cbar computations. The complete protocol's 128-bit proof-security level is NOT certified. Hash-expanding a small Fiat–Shamir seed into many Fp elements needs a defined domain-separated hash-to-field/PRG and its computational assumption; treating 8192 coordinates as automatically uniform under a short deterministic seed is not an information-theoretic statement.

### Exact independent toy verification [EXPERIMENT]

Toy K=F_29[theta]/(theta^4+theta+5) irreducible (verified in V14/V15), m5, beta16, 3 genuinely distinct toy extension challenges alpha=(28+theta),(5+theta+2theta²),(13+2theta+theta³), providing L=3*4=12 base-coordinate coefficient claims. Canonical a=(2,3,5,7,11), source third-field example modulus r=10007 and honest z_l=S_l mod29.

Reconstruct all 12 coefficient vectors by exact extension multiplication, and verify their honest quotients. For 75 independently seeded lambda∈F29^12, compute cbar, zbar, Sbar and kbar; all 75 EXACTLY satisfy Sbar=zbar+29*kbar, Sbar<10007, and native folded values equal <cbar,a> mod29.

Tamper ONE bound native z coordinate by +1 mod29. Residual e has one nonzero coordinate; exhaustive one, two, three independent fold rounds yield false accept counts exactly 1/29, 1/841, 1/24389. Additional nonzero dense error vector has exactly one accepting value among 29 for any fixed other coefficients, confirming the uniform-dot lemma without Monte Carlo. NO actual Pedersen, IPA, native Brakedown extractor, ZK or security implementation, so the toy verifies ARITHMETIC only.

Local script: /mnt/data/vfhe_v16_cross_factor_folding_gate.py SHA256 8f196a439ff50037ad69b0c5d4a8d53ceb967d129649b2f4b4a84f587be78d1e.
Local JSON: /mnt/data/vfhe_v16_cross_factor_folding_gate_results.json SHA256 1011e1368c0d8e7bbb1330dd74fae21f41c04217f57da707cba2d7658e988e8b.
Artifacts in runtime, NOT Git repository bytes.

### Research decision / V17 next one gate

**PASS:** cross-factor folding of many base-p linear link claims into one modular relation per independent challenge (ideal binding premises) is both algebraically complete and exactly 1/p-sound per round; it can radically reduce number of expensive per-linear-form GROUP MSM openings in V15's direct implementation model. Unlike V15, this is a concrete potentially helpful architecture under a sharply stated model.

**UNCLEAR:** It is not a completed knowledge-sound shared integer PCS. Explicit dense Fp coefficient folding remains O(km) per round, original Appendix F.2 native extraction unproved, source k factor digit linkage must be mapped, actual IPA and modular quotient CP proof not implemented, transcript/ZK/blinding/cost unmeasured. This technique resembles existing batched constraints/IPA; novelty is not established.

**NEXT_ACTION V17 (PI continuation only):** One decisive REAL INTERFACE feasibility check, not another synthetic error probability: read original ePrint 2025/286 Appendix F.1/F.2 and §3.1 encoding-to-CRT maps, and ascertain whether all k extension-factor digit vectors can be expressed as reductions/embeddings of THE SAME compact canonical integer vector a of length m. If different factors require distinct canonical message vectors of total dimension km, the V16 single length-m commitment assumption breaks and cost model must be revised. Alternatively if source mapping really identifies the same scalar digit in all factors, identify exact occurrence/equation in source and needed extractor (without claiming published exploit).
**End V16:** STATUS=PASS scoped batching algebra + quantified group-term saving; UNCLEAR real PCS and overall performance; STATE_UPDATE=YES independent vFHE only, global I192 frozen.


## 26. vFHE V17 — source CRT factor interface is NOT one automatically extracted scalar-digit witness (2026-10-14)

**One primary hypothesis (tested):** V16's L=d*(N/d) native CRT-factor links all arise from a *single, automatically shared and extracted* canonical integer digit vector a of length m, directly supported by the original ePrint2025/286 §3.1, §4.3, §5, Appendix E.2 and F.1/F.2, so we may interpret every CRT native factor value as a copy/embedding of the same a **without introducing a diagonal-range proof**.

**STATUS: FAIL automatic interface/extraction hypothesis; PASS explicit source-form CRT-idempotent contradiction to an implication in Appendix E.2 proof of Theorem 4.8.** A genuine scalar digit, if it exists, is diagonally embedded; **native field PCS/field-by-field lookup predicates do not force existence of that scalar digit**. V16's random folding mathematics remains correct for its stated IDEAL shared-a input, but m=1024 and its MSM numbers remain hypothetical, not yet mapped to source-native PCS objects. The original compiled/Fiat–Shamir SNARK has NOT been attacked or verified; official source PDF latest parity remains VERSION_UNVERIFIED. This is an independently checkable proof-level issue in the inspected source text, not author-confirmed erratum or established exploit.

### Original full-paper anchor, read directly from acquired PDF [FACT]

Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025 ePrint2025/286 (https://eprint.iacr.org/2025/286). Research MCP cache: 52 physical pages, GitHub ePrint mirror source SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, source kind github-mirror, latest version VERSION_UNVERIFIED.

- §3.1 physical p10: for each native p_i=1+(2N/d)*odd, ring R_(p_i)=Fp_i[X]/(X^N+1) decomposes as ∏_(j=0)^(k−1) R_(i,j), with k=N/d and R_(i,j)=Fp_i[X]/(X^d−ζ_i^(2j+1)) a field of order p_i^d.
- §4.3 physical pp20–21: coefficient-range TB consists of degree-<N polynomials with N **small canonical coefficient integers**; decomposition uses scalar digit subtable t_beta={0,...,beta−1} embedded diagonally into ring R_q. The target is htilde(i,j,k)∈t_beta as **ring elements**, not just componentwise field membership.
- §4.3 physical pp22–23: Lemma 4.6 is formulated for FIELDS, Theorem 4.8 claims PIOP soundness for the RING scalar t_beta membership; Remark 4.9 physical p24 acknowledges prior revisions involving beta<p_min and 2^(ell*)<p_min, but does not by itself establish diagonal component consistency.
- Appendix E.2 physical p48, *Proof of Theorem 4.8* explicitly makes the implication: if (t_beta,[htilde]) not in the ring lookup relation, then **there exists a field CRT projection Φ^(k)(htilde) not in t_beta**. This is algebraically false in products: ∏_k t_beta strictly contains the diagonal image of t_beta whenever at least two factors and beta≥2.
- §5 physical p25, Appendix F.1 p50: polynomial commitment to a ring polynomial f is the TUPLE of independent native field commitments to Φ^(i)(f), with per-field proving/evaluation. F.2 pp50–51 encodes rows of native matrices U_(Φ^(i)(f)) over separate native fields. These guarantee field-component opening consistency, not that component **values** are the same scalar integer digit.
- §5 physical p25 defines native Brakedown PCS matrix row dimension `m_PCS=2^(ell/2)` (ell even). This is NOT definitionally the hypothetical **integer digit vector length** `m_digit` used for V9–V16 cost examples. Thus V16's m=1024 has NO original-paper scale authentication merely from F.2.

### Exact minimal counterexample inside ONE source-form native prime [DERIVED / EXACT TEST]

Pick N=4,d=2,k=2 and native prime p=13=1+(2N/d)*3, with odd multiplier 3. In R=F13[X]/(X^4+1), choose fourth primitive root ζ=5; 5²=−1 mod13. Then

    X^4+1=(X²−5)(X²+5) mod13.

5 and −5=8 are NONSQUARE in F13; hence both quadratic factors are irreducible and

    R ≅ F_(13²) × F_(13²),

exactly the factor structure of original §3.1 at a small legal parameter point.

Set scalar Boolean subtable t_2={0,1}⊂R and ring element

    e(X)=7+4X² ∈R.

CRT projections: modulo X²−5, e=7+4·5=27=1 mod13; modulo X²+5, e=7−4·5=−13=0 mod13. Hence

    Φ(e)=(1,0) ∈ {0,1}×{0,1},

yet e∉{0,1} as a **RING ELEMENT**, because e has nonzero X² coefficient and is not equal to constant 0 or 1. Furthermore e²=e modulo X⁴+1; it is a genuine nontrivial CRT idempotent. This explicitly refutes the proof step

    h not∈ t_beta => EXISTS factor j with Φ_j(h) not∈ t_beta.

For ell*=1,beta=2, the source Theorem 4.8 side CONDITIONS beta<p=13 and 2^ell*=2<p=13 both hold. Take htilde constant e for all Boolean oracle rows; native factors see ordinary valid constant Boolean 1 and 0, while the ring scalar table relation fails. This is stronger than merely complaining that the general proof omitted a diagonal condition.

**CAVEAT:** The concrete test directly verifies FALSE implication and the possibility of each native component being individually valid. It does NOT execute all PIOP sum-check/Fiat–Shamir rounds. Fieldwise completeness and CRT lifting of ideal-oracle prover messages suggest a more extensive **candidate** full ideal-PIOP falsifier, but this still requires a checked transcript and any auxiliary constraints, and does NOT establish a real deployed SNARK exploit.

### Two logically distinct legitimate integer interfaces [DERIVED]

1. **Scalar table digit:** If a_j∈[0,beta−1]⊂Z, then Φ_(i,h)(a_j) is exactly that same embedded scalar a_j in EVERY CRT factor. One common vector a of length m_digit is conceptually the desired semantic relation, BUT imposing it from independently committed field vectors is exactly the unresolved R_diag cross-factor linking goal. It is **circular** to assume this common a has been extracted in order to justify the proof that needs to enforce its existence.
2. **General ring-valued coefficient vector:** A ring element f(X)=Σ_(t=0)^(N−1) f_tX^t is described by N canonical coefficients (subject to q/range). Its CRT-field images are f mod (X^d−ζ^(2j+1)): **factor-dependent linear combinations** of the N coefficients, not copies of a single per-factor scalar digit. Exact toy example f=2+3X+4X²+5X³ at N4,p13 gives its two F13²-coordinate vectors (9,2) and (8,4). One can potentially commit to an N-dimensional *canonical coefficient vector* and link its publicly defined factor-dependent linear transforms, but it is NOT V16's same-scalar-digit c_lj mapping without change.

The original source combines these two object levels: TB imposes canonical COEFFICIENT range for ring v, then h decomposes each coefficient into SCALAR digits t_beta. The native F.2 polynomial matrices are still another object over separate CRT fields. Consequently V16 folding remains a useful **abstract batch gadget** but its dimension/cardinality/per-prime cost requires an actual occurrence map and source-specific extractor. For unstructured general ring-valued witness of s ring elements, coefficient witness dimension can be N*s rather than a chosen m_digit=1024, while a genuine scalar digit witness across many indices has whatever total number of digit slots occurs in §4.3—not necessarily native Brakedown m_PCS.

### Minimal exact, independently rerun script [EXPERIMENT]

`/mnt/data/vfhe_v17_crt_factor_interface_audit.py` SHA256 `ef95aa14980245ea65e693a0be690970e7e6e4ed692a15ee98a453219d95aabd`; JSON `/mnt/data/vfhe_v17_crt_factor_interface_audit_results.json` SHA256 `2e7ddf329a0f4546c046b328591236c1c82e8d83d396d323e41d9206a5f2d33a`. Local files (not Git bytes). Script independently computes factorization/irreducibility via quadratic nonresidues, ring multiplication with X⁴=−1, e²=e, projections (1,0), nonmembership e in ring {0,1}, source small-parameter congruence, and factor-dependent coefficient-vector projections. Ran twice, same hashes. No real PCS proof, ideal PIOP transcript, SNARK, or security exploit.

### Research decision / next minimal falsifier

**FAIL** interpreting all original factorwise committed field-values as AUTOMATIC SAME canonical scalar digit vector, and FAIL transferring V16's m1024 single-length-m MSM count to source workload without mapping. Theorem 4.8 Appendix E.2 proof contains a specific formally incorrect implication for the inspected version. This is a genuine source-anchored algebraic objection, not confirmation that the final compiled protocol is insecure.

**NEXT_ACTION V18 only if PI continues:** one focused **source-accurate IDEAL-PIOP transcript test** for the e=(1,0) CRT idempotent, targeting Π_beta_range Fig.1 §4.3 and Appendix E.2: instantiate fieldwise honest memory-counter and grand-product oracles for each factor, glue with CRT, and check every ring verifier identity for an INVALID scalar-ring lookup instance. Include β<p_min and 2^ell*<p_min, and distinguish ideal oracle from PCS/F-S; if actual scheme has an explicit diagonal check, identify it and revise attack. If the invalid transcript passes, separate theorem/protocol soundness finding from contribution decision, then evaluate minimal source-specific fix. No implementation of unrelated PCS architectures in this iteration.

**END V17:** STATUS=FAIL automatic source interface / PASS exact p13 source-form idempotent and counterexample to Appendix E.2 implication. STATE_UPDATE=YES independent V-series, general I192 unchanged.


## 27. vFHE V18 — source Figure-1 beta-range IDEAL PIOP accepts a non-diagonal CRT idempotent

Date: 2026-10-14. Independent vFHE V18. Global/general FHE iteration I192 remains FROZEN. Human PI controls publication/security-disclosure decisions.

**Primary falsifiable hypothesis:** V17's incorrect proof implication in Appendix E.2 is a harmless proof gap because, despite fieldwise-valid digit projections, the published Figure 1 Pi_beta_range ideal verifier's REAL memory counters, grand-product tree or two sum-check identities necessarily reject the ring-INVALID non-diagonal idempotent e=(1,0). ONE minimal decisive test: source-faithfully commit native factorwise honest counters BEFORE sigma/tau, CRT-glue oracles, construct the four product-tree oracles AFTER sigma/tau and BEFORE chi/rho/xi, explicitly perform both degree-3 sumchecks, and check every Figure-1 verifier identity on an invalid ring-valued beta lookup.

**STATUS: FAIL the "harmless proof gap" hypothesis. PASS a complete minimal Figure-1 IDEAL Pi_beta_range adversarial transcript passing for EVERY allowed challenge, with an exact algebraic identity and two 1-round sumchecks tested. The source statement is FALSE, so this is a scoped ideal-PIOP SOUNDNESS COUNTEREXAMPLE. Not a real compiled PCS/Fiat–Shamir SNARK exploit, nor yet a full Pi_range+Pi_decomp/CKKS computation transcript. Security relevance is material but official latest PDF revision remains VERSION_UNVERIFIED. Novelty relative to known CRT rectangular-vs-diagonal observations is NOT established.**

### Paper facts/provenance [FACT]

Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286, https://eprint.iacr.org/2025/286. Read via Research MCP cached full 52-physical-page github-mirror PDF, SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, version_status VERSION_UNVERIFIED.

- §3.1 physical PDF p10 ring CRT and p=1+(2N/d) a for odd a.
- §4.3 physical p22 Lemma4.6 constructs read_ts and final_cts counters per table value, Eqs24–26 define WSt/WSh/RS/S.
- §4.3 physical p23 Figure1 specifies first oracle commit (read_ts/final_cts), THEN sigma,tau, THEN four product-tree oracle polynomials f^(1), THEN chi/rho/xi, THEN two sumcheck PIOPs and final grand-root check. Theorem4.8 p23 states beta<p_min and 2^ellstar<p_min and PIOP knowledge error O((2^ellstar+2^(b/c))/|S|).
- Appendix E.2 pp46–49, esp. p48, contains the false inference "if ring h is not in scalar table, one CRT projection must not be in scalar table"; it also defines the two virtual sumcheck oracles g_{chi,rho} and the grand-product invariant.
- F.1/F.2 pp50–51 compiles field projections to per-field PCs; no evidence yet of concrete Fiat–Shamir success.
- A separate public web PDF cache sometimes resolves to a 50-physical-page older revision, so physical page labels and theorem text must NOT be silently mixed. This V18 proof specifically targets the 52-page SHA256 above. Mathematical expressions were checked against text extraction; complex glyph transcription still warrants independent visual/source-authenticated validation before author notification.

### Malicious statement and theorem side conditions [DERIVED]

Use N=4, d=2, p=13=1+(2N/d)*3 (odd 3), k=2. R=F13[X]/(X^4+1)≅F_(13²)×F_(13²) since X⁴+1=(X²−5)(X²+5), both quadratic factors irreducible mod13. Let

    e(X)=7+4X²,  e²=e, e≠0,1, and Phi(e)=(1,0).

Take beta=2 (t_beta={0,1}), ellstar=1, b/c=1. Conditions beta=2<p_min13 and 2^ellstar=2<13 are satisfied. Commit to ring multilinear htilde(T)=e with two Boolean values h(0)=h(1)=e, BOTH outside scalar table t_2. Thus the verifier's lookup statement is FALSE.

### Prover round 1, BEFORE sigma/tau: genuine per-field counters CRT-glued [DERIVED]

Fixed ring oracle Boolean evaluation arrays:

    read_ts(0)=0,  read_ts(1)=1,
    final_cts(0)=2(1−e), final_cts(1)=2e,
    t_beta(0)=0, t_beta(1)=1.

Extend read_ts(T)=T and final_cts(T)=2(1−e)(1−T)+2e T as ring multilinear polynomials, COMMITTED BEFORE challenge selection. In factor R1 where e=1, honest reads from table DIGIT1 twice: read counters (0,1), final counters (table0:0, table1:2). In factor R2 where e=0, honest reads table DIGIT0 twice: reads (0,1), finals (table0:2,table1:0). CRT-glued final_cts are NOT globally ordinary integer counters, but Figure1 checks only ring algebra and never constrains these to diagonal scalar integers. This is the missing invariant; source prose "constructs counters" is not a verifier check.

### Prover round 2, AFTER sigma/tau: exact ring grand products [DERIVED]

Using exactly source Eqs24–26 and h(i)=e:

    WSt=(-tau)(1−tau),
    WSh=(e+sigma−tau)(e+2 sigma−tau),
    RS=(e−tau)(e+sigma−tau),
    S=(2 sigma(1−e)−tau)(1+2 sigma e−tau).

In free commutative polynomial ring, direct symbolic expansion yields

    WSt*WSh−RS*S
      = 2e sigma(e−1)(e+sigma−tau)(2e sigma−2 sigma tau+1).

Because e(e−1)=0 in R, identity WSt*WSh=RS*S holds for EVERY sigma,tau in R, even zero divisors and non-base-field challenges. No Schwartz–Zippel hit or hash collision is required.

Construct FOUR source Figure1 product-tree oracle f_alpha^(1) for alpha in {WSh,RS,WSt,S}. Each has two leaves v_alpha(0),v_alpha(1) from above and parent oracle Boolean table:

    f_alpha^(1)(0)=v_alpha(0)*v_alpha(1), f_alpha^(1)(1)=0.

For ellstar=1 the second value is unused padding. This satisfies the paper's binary product recursion for i=0 and i=1, where i=1 has zero parent and zero right child; multilinearly interpolate each table. Each f_alpha^(1) is fixed after sigma/tau and before later challenges.

### Prover round 3, AFTER chi/rho/xi: exact two degree-3 sum-checks [DERIVED / COMPUTED]

Source Figure1 virtual oracles h*(T) and t*(T) sum weighted binary product-gate discrepancies, with equality-polynomial factors eq(rho,T),eq(xi,T) and independent chi. The constructed four binary product-tree relations hold at both T=0,1, hence

    h*(0)=h*(1)=0,   t*(0)=t*(1)=0

for ALL chi,rho,xi in the ring. For ellstar=b/c=1 each is a polynomial in T of degree≤3. Honest univariate sumcheck prover sends the exact coefficient polynomial g(T)=h*(T) or t*(T); verifier checks g(0)+g(1)=0, samples r, checks g(r) against final virtual-oracle evaluation from authenticated ring oracle evaluations. Both pass for ANY choice of challenges. The grand-root equality already holds identically. The transcript is malicious only about the scalar-table witness, not about satisfying Figure1 algebraic checks.

**NUMERICAL INDEPENDENT TEST:** Implemented actual ring R=F13[X]/(X⁴+1), modular polynomial arithmetic with X⁴=−1, exact factor projection, full fixed ring oracle arrays, 4 Figure1 leaf formulas, 4 root products, full two-layer polynomial tree f^(0),f^(1), two virtual g polynomials, direct degree3 Lagrange/Vandermonde interpolation, exact one-round sumcheck identities and randomly sampled final oracle evaluations. Tested 100 deterministically seeded transcripts with full ring-valued sigma,tau,chi,rho,xi,sumcheck_r (not only scalar subfield), ALL PASS. Reexecuted twice; SHA256 of script/results stable. Tests are sample evidence; the universal acceptance follows from algebraic source-protocol construction.

Local script:
    /mnt/data/vfhe_v18_ideal_piop_transcript_gate.py
    SHA256 c4af962733eb50856d4ec45147eb5e56edf63a21316ed5ea26267dba989d13d1

JSON:
    /mnt/data/vfhe_v18_ideal_piop_transcript_results.json
    SHA256 06fce2710687bf53018b2b30ae158589bd9aa70900b7dd341ba7db66708b67b8

No PDF or code was committed to Github; only this archived research NOTE. No actual Merkle, Brakedown, native PCS, Fiat–Shamir, zero-knowledge, knowledge-extractor or CKKS proof implementation.

### Interpretation and decision

**PROVEN, scoped:** Theorem4.8's stated ideal Pi_beta_range soundness is FALSE for the inspected 52-page mirror version's Rq scalar-lookup relation when the CRT product has at least two factors. An invalid oracle is accepted with probability ONE by the displayed source Figure1 algebraic protocol. Since the construction uses a nontrivial CRT idempotent, the phenomenon generalizes to larger admissible ring CRT products; p13 is only the smallest explicit source-form toy.

**NOT PROVEN:** The real cryptographically compiled SNARK is exploitable; the entire outer Pi_range in §4.3 with Pi_decomp is broken under an authenticated final version; an actual end-to-end vFHE ciphertext can be forged; performance of a patch or publication novelty. The clean ideal protocol failure is nevertheless stronger than the old isolated proof-implication gap.

**NEXT_ACTION V19 (on PI continuation only):** ONE source-faithful EXTENSION of this invalid Pi_beta_range witness to the full outer Pi_range (Eq22 decomposition, Figure1, Pi_decomp) for a ring value with an invalid small COEFFICIENT range, without inventing a hidden digit-to-coefficient link. If that passes, a falsified coefficient-range proof is closer to the CKKS high-level validation interface. Retain separate source PDF version warnings and privacy/soundness distinctions. After that, before contacting authors, verify exact official/version-equivalent source and independent formal transcript review, and let human PI decide disclosure.
**END V18:** STATUS=PASS complete Figure1 ideal PIOP counterexample; STATE_UPDATE=YES; global I192 frozen.


## 27. vFHE V18 — CRT-lifted dishonest ideal PIOP Figure 1 transcript

Date: 2026-10-14. Independent vFHE V18; global I192 frozen.

**One hypothesis / decisive test:** Does the p13,N4,d2 idempotent from V17 extend from one false implication in source Appendix E.2 to a valid transcript satisfying ALL ideal-oracle algebraic verifier constraints in paper Figure 1 Π_beta_range, for an invalid t_beta={0,1} ring lookup? Distinguish ideal oracle algebra from compiled PCS/SNARK and Theorem4.8 quantitative soundness at concrete tiny security.

**STATUS: PASS exact constructed dishonest ideal-IOP algebraic acceptance**, subject to the precise scope: fieldwise honest grand-product/memory prover oracles glued via CRT, transcript's claimed lookup is false in ring, yet Fig1 grand products, final root identity and both Boolean-domain sumcheck polynomial SUM claims hold for every verifier challenge (checked exhaustively for a subset and proven by CRT). This refutes soundness of the SOURCE-SPECIFIED ideal oracle relation in this model. Does NOT verify a real compiled Brakedown PCS, FS transform, non-oracle implementation, 128bit concrete soundness or official current PDF version.

**Original source [FACT]:** Cascudo et al. *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286. Cached 52pp GitHub mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, official latest parity VERSION_UNVERIFIED. §3.1 p10 CRT factor decomposition; §4.3 p22 Lemma4.6 field memory-counter, pp22–23 Fig1 Π_beta_range 3 rounds; Thm4.8 p23 β<p_min and 2^ellstar<p_min; Appendix E.2 physical p48 gives false 'some field factor outside scalar table' inference. Figure1 explicitly has prover precommit read_ts,final_cts BEFORE verifier sigma,tau, then prover constructs GP f oracles BEFORE verifier chi,rho,xi, then two sumcheck protocols verify zero sums. No additional diagonal-equality step found in these inspected protocol lines. This is an ideal PIOP finding for inspected edition, not an exploit against another edition.

**Counterexample [DERIVATION]:** N4,d2, p13=1+(2N/d)*3, ellstar1, beta2. R=F13[X]/(X4+1)≅F13²×F13² via (X²−5)(X²+5). e=7+4X² maps CRT (1,0), e²=e, e not in scalar {0,1}. Let htilde be constant polynomial e, so BOTH Boolean inputs htilde(0)=htilde(1)=e and the original ring t2 membership relation is FALSE. Source Theorem4.8 side bounds beta2<p13 and 2^ellstar2<p13 hold. Native components see honest lookup digits (1,1) and (0,0).

**Memory counters BEFORE sigma,tau:** One R-valued read_ts oracle has Boolean leaves (0,1). CRT field component1 has two accesses to table digit1, component2 two accesses to table digit0. Their legal final-count tables are component1 (0,2), component2 (2,0). CRT glue into ONE R-valued final_cts oracle with leaves [2(1−e),2e] (in two field-coordinate pairs [(0,2),(2,0)]).

**After sigma,tau:** Figure1's four corresponding 2-leaf vectors, writing products of elements in commutative R:
 WSh leaves: (e+sigma−tau,e+2sigma−tau);
 RS leaves: (e−tau,e+sigma−tau);
 WSt leaves: (−tau,1−tau);
 S leaves: (−tau+2sigma(1−e),1−tau+2sigma e).
The ring product equality WSt·WSh=RS·S holds identically in R for EVERY ring sigma,tau, by applying CRT into the two fields and using memory-count equality. Explicit sigma,tau can be arbitrary ring elements; the proof is per-component, not dependent on integer challenges or exceptional-set sampling.

**Grand-product oracle tables:** For ANY 2-leaf values (v0,v1) in R, define a polynomial via its 2x2 Boolean interpolation table
 f(0,0)=v0; f(0,1)=v1; f(1,0)=v0*v1; f(1,1)=0.
This implements source Lemma4.7's recursion at both input bits i=0 and i=1:
 f(1,0)=f(0,0)f(0,1), f(1,1)=f(1,0)f(1,1)=0;
 and root f(1,0)=P.
For each of the four products choose its corresponding f as Fig1's grand-product oracle after sigma,tau and BEFORE chi,rho,xi. Resulting virtual sums over Boolean X of
   [f_WSh(1,X)−f_WSh(X,0)f_WSh(X,1)+chi*(f_RS(1,X)−f_RS(X,0)f_RS(X,1))]*eq(rho,X)
 and analogously for WSt,S with xi, are exactly ZERO because the GP recursion defects vanish for EACH Boolean X. Thus BOTH requested sumcheck zero targets are TRUE polynomial sum statements; ideal sumcheck prover can answer all challenges honestly (the interpolated polynomial may be nonzero outside Boolean hypercube, but that is expected and sumcheck checks the sum, not pointwise zero away from Boolean inputs). The final root equality is also true. All verifier queries access the same pre-specified/interpolated R-valued oracles.

**Ordering:** read_ts and final_cts fixed before sigma,tau; f_WSh,f_RS,f_WSt,f_S selected after sigma,tau, before chi,rho,xi, as required; virtual-oracle sumcheck uses previously fixed polynomials. No challenge-dependent redefinition of previously bound oracles.

**Exact experiment:** /mnt/data/vfhe_v18_ideal_piop_crt_attack.py SHA256 e80af660f6b79d7da47fd11cc6eb7a4efa4ff3271f622659ec456c0affe534e3; JSON /mnt/data/vfhe_v18_ideal_piop_crt_attack_results.json SHA256 d68f436ad2308b6d9b81edf2b23e43df49ab1864ef0438efc7e43edc8765704b. Standard Python. 676 test configurations include all 13² base-scalar sigma,tau with 3 chi/rho/xi combinations, plus 169 mixed-component ring sigma/tau choices. Each verified four GP recursions, final root product, two virtual Boolean-sum defects, false scalar table membership, true all factor table membership. The symbolic CRT reasoning establishes truth for all ring challenges, not just the 676 tested.

**Potential subtleties / scientific restrictions:** Source PDF extraction may distort Figure1's indices, but current construction matches Lemma4.7 printed recursion and factor-level honest memory counter semantics. Need independent TEX/rendered-PDF check before author-facing claim. The calculation does not independently implement a generic interactive sumcheck transcript at each random verifier challenge; it proves its claimed sum identity true, which suffices for existence of a perfectly complete ideal sumcheck prover. This construction depends on the SOURCE-SPECIFIED ideal-oracle model; source's polynomial commitment implementation and any external cross-field constraints not tested. Avoid asserting full final SNARK compromised or that cited authors have not already patched a newer version. The very small toy p13 has no meaningful 128bit parameters, although algebraic acceptance is identity and its CRT mechanism extends abstractly whenever the ring has at least two field factors.

**Decision:** PASS transition from proof-step error (V17) to source-specified ideal oracle algebraic soundness failure. Full cryptographic exploitation status UNCLEAR / HUMAN_REVIEW. No proactive disclosure without human PI decision.

**NEXT V19 on PI continuation:** ONE decisive external-source / compiled-interface gate: inspect original §2.2 PCS compilation and F.1/F.2 oracle commitment binding for whether any global scalar-table representation consistency is additionally enforced; prove or disprove that CRT-glued oracles can be committed/extracted as one ring polynomial without a diagonal check. If not, document precise obstruction; if yes, formulate bounded, reproducible adversarial transcript and possible minimal fix. In parallel confirm ePrint newest author version provenance as necessary; do not silently change source edition.

**END V18:** STATUS PASS ideal Fig1 counterexample; RESULT CRT-glued prover memory counter, GP and sumcheck true identities for invalid ring table input; STATE_UPDATE YES, vFHE V-series only; global FHE I192 frozen.


## 28. vFHE V19 — F.1/F.2 split-field PCS compiler does not supply scalar-digit diagonal binding (2026-10-14)

**PRIMARY hypothesis and decisive test.** Could the original paper's §2.2 general PIOP→argument compiler or its §5 / F.1 / F.2 / F.3 per-field PCS encoding add a cross-factor **scalar-digit diagonal consistency** check that prevents the V18 invalid-ring-digit, accepted-ideal-PIOP oracle family from being committed, opened, or correctly extracted as a ring polynomial? One decisive test: inspect ALL original compiler operations and construct a *source-matching toy* F.1 combined PCS with genuine extension-field F.2 native Merkle column/linear consistency and F.3 piecewise [2,1] RS for every V18 prover oracle.

**RESULT: FAIL proposed implicit-compiler-repair hypothesis; PASS source-specified interface compatibility and exact toy PCS proof checks.** This is NOT a deployed or source-library compiled SNARK attack and not a proof of cryptographic 128bit insecurity in the final author edition. A successfully extracted ring polynomial is NOT necessarily a small scalar digit; the compiled PC argument may have excellent ring binding while the ring lookup predicate is still false. Standard PCS completeness makes the accepting ideal-oracle transcript capable of honest polynomial-evaluation openings, so the inspected interface offers no new semantic obstruction. **STATE_UPDATE YES** to independent V-series only; global I192 frozen.

### Actual source interface (not inference) [FACT]

Paper: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint2025/286. Acquired 52 physical page Research-MCP GitHub mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest edition parity VERSION_UNVERIFIED.
- §2.2 **physical p9**: compile ring PIOP by replacing each R-valued oracle with polynomial commitment; replace evaluation queries by claimed value + PC evaluation proof. Nothing says every oracle output must be in canonical scalar table; proof system relies on SOUNDNESS of original PIOP.
- §5 **physical p25**, F.1 **p50**: \(R_q\cong\prod_i F_i\), \(\mathrm{Com}(f)=(\mathrm{Com}_i(\Phi_i(f)))_i\). Evaluation/verifier accepts if every field eval \(y_i=\Phi_i(f)(a_i)\) passes. Their binding/knowledge-soundness claim concerns **any ring polynomial**, not the diagonal subset \(t_\beta\).
- F.2 **physical pp50–51**: native field matrix \(U_f\), each row encoded by field-linear Enc, Merkle authenticated encoded **columns**; testing checks \(\mathrm{Enc}(r U_f)|_Q=r\widehat U_f|_Q\); evaluation checks \(\mathrm{Enc}(q_1 U_f)|_{Q'}=q_1\widehat U_f|_{Q'}\), \(y=\langle q_1 U_f,q_2\rangle\). No global cross-CRT scalar digit equality predicate appears in these concrete tests.
- F.3 **physical pp51–52**: when m≥N/2, split input vector into blocks of length N/4 and encode each via \([N/2,N/4]\)-RS, then concatenate. At toy N=4,mPCS=2, this is two [2,1] evaluations, i.e. Enc([a,b])=[a,a,b,b], length M=4. This is a genuine small parameter case of the paper's *piecewise RS* blueprint, not its large-parameter instance.

**Fundamental semantic lemma [DERIVED]:** Under the exact CRT ring isomorphism \(R\cong F_1\times F_2\), \((f_1,f_2)\) uniquely determines some ring polynomial f. A binding commitment to each \(f_i\) therefore binds one legitimate ring polynomial f; there is no mathematical need to require \(f_1=f_2\). But the **scalar digit** subtable \(t_\beta=\{0,1,...,\beta-1\}\subset R\) maps to the DIAGONAL tuples \((a,a)\), strictly smaller than \(\prod_i t_\beta\). Thus the compiler can be fully correct as a **ring polynomial commitment** while providing ZERO missing diagonal-table-membership guarantee. PCS soundness cannot repair an unsound PIOP semantic relation merely by binding/extracting its arbitrary ring-valued oracle.

### Exact toy PCS interface test [EXPERIMENT]

Keep V17/V18 legal source-form ring \(R=F_{13}[X]/(X^4+1)\cong F_{13^2}^{(u^2=5)}\times F_{13^2}^{(u^2=8)}\), N4,d2,p13, β2, and \(e=7+4X^2\mapsto(1,0)\), \(e^2=e\), \(e\notin t_2\).
- Fix V18 *pre-challenge* oracles h (Boolean lookup values e,e), read_ts (0,1), final_cts (2(1-e),2e); the scalar table is public. After ring sigma,tau, use V18 fieldwise-honest WSh, RS, WSt, S values and construct four associated 2-variable GP multilinear oracles.
- The F.2 description assumes *even* MLE arity ell for square matrix; pad one-variable oracle with an independent dummy Boolean variable, preserving ALL original oracle values, so each relevant field polynomial uses a 2×2 evaluation matrix U_f. The 4 actual GP oracles already have two variables. The public scalar table is tested as a read-only oracle too.
- For each of TWO factors, implement actual extension-field arithmetic in F13[u]/(u²−5), F13[u]/(u²−8); execute piecewise-RS Enc([a,b])=[a,a,b,b] for BOTH matrix rows; use SHA256 Merkle leaves encoding full *columns* of the 2×4 encoded matrix, root per (oracle, factor), authenticate all 4 openings and reject modified leaf.
- Native F.2 testing for arbitrary random field extension coefficients r∈F_(13²)²: verify on EVERY column \(\mathrm{Enc}(rU_f)|_Q=r\widehat U_f|_Q\) (Q=all four); evaluation phase: choose random native extension point x,y, derive \(q_1=(1-x,x)\), \(q_2=(1-y,y)\), evaluate \(v'=q_1 U_f\), verify all Enc(v') query equalities and actual MLE \(f(x,y)=\langle v',q_2\rangle\).
- Repeat with 64 seeded ring sigma/tau choices (including true extension-field coefficients), **8** oracle names per instance (h,read_ts,final_cts,public scalar table,4GP) and **2** native factors; 64·8·2·4·2 = **8192** Merkle-authenticated field coding checks. All PASS, all altered-leaf authentication attempts fail. All 64 native point evaluations PASS, ring CRT values remain consistent. In EVERY instance the initially committed h value e is **not** a member of the scalar ring table {0,1}.
- Asymptotic security NOT measured; this is exact algebra/encoding/Merkle IO, not a fully implemented Brakedown extractor or the entire source PIOP-to-SNARK compiler; 13-bit toy characteristic not 49bit.

**Reproducible local artifacts (not Git repository):** `/mnt/data/vfhe_v19_pcs_compiler_interface_gate.py`, SHA256 `32f3964ca023c58aefddd1c4e83c51de7ffd7c17d80a377c51235f6cba3f04fa`; `/mnt/data/vfhe_v19_pcs_compiler_interface_results.json`, SHA256 `9afabaa9ffec407e0d401d98d1afc54da5c4b38a181206a6537cfaa961057d9f`. Both execution reruns exactly identical digests.

### Version and scope warning

A web-search-cached PDF reference for the public eprint URL presented **50 pages** and retained early "Authors Suppressed" running headers, whereas the Research-MCP authenticated-on-GitHub mirror contains **52 pages** with explicit Theorem4.8 Remark4.9 caveats. The public search cache is not evidence of the live PDF's revision; direct download to authenticate current official version FAILED. An author publication page https://antonioguimaraes.org/publication/cascudo-verifiable-2025/ points to the work but does not furnish a cryptographically version-matched PDF. Do not claim that current official, CRYPTO proceedings final, or a deployed system is confirmed affected. The 52pp inspected source is the only edition to which the current concrete technical claim is attached.

### Decision / NEXT_ACTION

**PASS:** no implicit diagonal scalar-table extraction or range statement appears in the inspected PCS compiler; exact native field commitments and evaluations for V18 dishonest ring digit can be HONEST and complete. This identifies a SOURCE-SPECIFIED ideal-IOP/PCS interface soundness gap. A secure binding PC cannot enforce a property not stated/tested.
**UNCLEAR/HUMAN_REVIEW:** exact live official version, full compiled malicious SNARK transcript and FS, arbitrary 49bit parameter instantiation, original outer Π_range completeness/soundness, ultimate CKKS vFHE exploit, disclosure strategy or mathematical novelty.

**V20 next ONE falsifier (only if PI continues):** Stop repeated generic PCS checks. Construct a FALSE **outer** \(R_{\mathrm{range}}\) instance whose ring coefficient violates [0,B−1], and an exact V18-style CRT-glued \(h\) satisfying source Eq.(22) decomposition and Fig1 inner digit lookup, so complete Π_range (Π_decomp + Π_beta_range) accepts in ideal oracle model. This is the shortest next test toward original CKKS range semantics. Use small N4, B4, β2,c2, and isolate any Eq.(22) obstruction. If possible, then prioritize independent source edition authentication before any author-facing disclosure.
**END V19:** STATUS PASS source PCS interface + exact toy; NEXT V20; STATE_UPDATE YES independent vFHE only, GLOBAL I192 frozen.


## 29. vFHE V20 — full outer Pi_range accepts a coefficient-invalid CRT idempotent (2026-10-14)

**Primary falsifiable hypothesis [H-V20]:** V18's ideal `Pi_beta_range` gap is harmless for actual `Pi_range`, since source Eq.22 / `Pi_decomp` forces each output **ring coefficient** into the genuine range `[0,B-1]`, regardless of per-CRT-field scalar-digit validity.

**ONE decisive full ideal-PIOP test [FAIL hypothesis / PASS constructed counterexample]:** ePrint2025/286, cached 52 physical pages SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED**. Original source §3.1 physical p10; §4.3 Lemma4.3/Eqs22–23 pp20–21, Figure1/Theorem4.8 pp22–23, Appendix E.2 pp47–49. Use source-form `R=F13[X]/(X^4+1)=F13²×F13²` and nontrivial idempotent `e=7+4X²→(1,0)`. Set **outer** coefficient bound `B=4,b=2,c=1,beta=4`, index length `ell=1`, `nu=2,gamma=0,ellstar=3`. Conditions `beta=4<13` and `2^ellstar=8<13` hold. The claimed output MLE `v_tilde(i)=e` for Boolean `i∈{0,1}` **violates** coefficient-range table `T_4` because e has coefficient 7 and coefficient 4. One committed 3-variate digit oracle `h_tilde(i,j0,j1)=e` if `(j0,j1)=(0,0)`, else 0, satisfies original Eq22 *exactly* for all i (even non-Boolean r_i), so `Pi_decomp` has an **HONEST accepting** degree-2 sumcheck. But h has two non-scalar digit e values and six zeros; its factors see genuine scalar-digit multiset `{1,1,0×6}` and `{0×8}`.

**Prechallenge memory & Figure1 completeness [DERIVATION]:** Make truly honest `read_ts` counters per CRT field in Boolean lexicographic h-access order, with source table t_beta={0,1,2,3}. Final counts in factor1 `(6,2,0,0)` and factor2 `(8,0,0,0)`. Entrywise CRT glue with `e` gives ring-counter final table `(8−2e,2e,0,0)`. These oracles are fixed **BEFORE** sigma,tau. Every factor has a perfectly correct field memory transcript, so the ring grand-product identity `WSt*WSh=RS*S` holds as a **polynomial identity** for all sigma,tau. After these challenges, produce all four original Quark-style flattened binary `f_alpha^(1)` product-tree ring oracles. Source Figure1 `g_{chi,rho}` virtual discrepancies sum to zero on all Boolean positions; the two prescribed degree-3 sumchecks pass for any chi,rho,xi and subsequent sumcheck challenges. The *outer* decomp sumcheck passes on the true Eq22. There is no challenge-collision event: the invalid coefficient-range statement is accepted with probability one by the **displayed ideal Pi_range algebraic verifier**.

**Exact computational reproducibility [EXPERIMENT]:** Pure Python finite quotient arithmetic `R=F13[X]/(X^4+1)`, no numerical approximation or cryptographic libraries. 16 deterministically seeded full transcripts with random whole-ring sigma,tau,chi,rho,xi and sumcheck challenges all **PASS**. Verifies false actual coefficient statement, true Eq22 at random ring input, both true field memory arrays, correct four ring product-tree Boolean relations/root equality, both inner sumchecks with exact degree-3 interpolation and verifier final MLE queries, and outer degree-2 sumcheck with final MLE evaluation. The universal theorem follows from CRT-glued honest field transcript identities, not from 16 random samples.

**Files:** `/mnt/data/VFHE_V19_Outer_Range_PIOP_CRT_Counterexample_2026_10_14.md` SHA256 `8defd3ae3aa43f3942446b3044b810dc9250f21ece693fa9eb5b4c328c22362f`; script `/mnt/data/vfhe_v19_outer_range_ideal_piop_gate.py` SHA256 `c8f6b8689a307a6699c42fcc77d6434d112cd2e5660741d9c7a8fa010e52f4fe`; JSON `/mnt/data/vfhe_v19_outer_range_ideal_piop_results.json` SHA256 `246bb8d273c6087839e454e1f96850b62e48606a788b60f3c2080c80d5590130`.

**Caveats:** NOT a demonstration of a real compiled PCS/Brakedown/Fiat–Shamir SNARK exploit, authenticated latest publication flaw, false full CKKS execution proof, 128-bit attack, deployable forgery, or novel patch. Basic per-factor root equations `prod_(digit=0)^{beta−1}(h−digit)=0` also accept this bad idempotent and do not repair the missing CRT diagonal condition. Exact final-source PDF parity and independent manual inspection of garbled figure typography remain evidence gates before author contact.

**END V20:** STATUS=PASS explicit ideal **outer coefficient-range** false-statement accepting witness; source version and compiled security HUMAN_REVIEW. **NEXT_ACTION V21:** independently authenticate the latest exact author/proceedings edition and visually verify Figure1 product-tree indexing, then investigate whether the actual compiled PCS/Fiat–Shamir proof adds any soundness/binding condition not present in source Pi_range/F.1–F.3. Verify official version and method independently before contacting authors; only PI can authorize disclosure or pivot. **STATE_UPDATE=YES:** vFHE V20 completed, general I192 remains frozen.


### Independent V20 reproduction — 48 exact sumcheck transcripts

**2026-10-14 independent replication of existing V20 note, read-before-write:** The cumulative technical archive already contained the original V20 result while standalone state remained at V19. We therefore DID NOT create a second numbered V20 hypothesis or rename existing records. We independently reimplemented the same one-test falsifier in a fresh Python program, with an explicit verifier for all three polynomial sumchecks and exact interpolation over source ring R.

**[SOURCE]** §4.3 p20–23 Eq22, Fig1, Lemmas4.3–4.7, Thm4.8 of cached 52-page ePrint2025/286 mirror; PDF version equivalence to current IACR/CRYPTO official edition still VERSION_UNVERIFIED.

**[INDEPENDENT DERIVATION]** Choose p13,N4,d2, B4,b2,c1,beta4, ell1, nu2,gamma0,ellstar3. p=1+(2N/d)·3; p>beta and p>2^ellstar=8. e=7+4X² is idempotent with CRT projections (1,0), but its coefficient values 7 and 4 violate [0,3]. Set v(0)=v(1)=e and h(i,j)=e iff j=0, else 0. Eq22 and all its MLE extensions hold exactly. Actual native lookup counters are factor1 final(6,2,0,0), factor2 final(8,0,0,0); CRT-lift final(8−2e,2e,0,0), fixed pre-(sigma,tau). Product-tree oracles use source f(1,i)=f(i,0)·f(i,1), root f(1,1,...,1,0), and both virtual Fig1 sumcheck sums are exactly zero. The outer Pi_decomp sumcheck has true target e. This is a false-coefficient statement with an accepting source ideal-IOP transcript, not a cryptographic commitment attack.

**[EXPERIMENT]** Fresh standalone Python in THIS session:
- `/mnt/data/vfhe_v20_outer_range_independent_gate.py` SHA256 `72a6fc7f55352b121e8866d3f5aa67642e905a7d845f6faced3dd977ae9b2f5c`.
- `/mnt/data/vfhe_v20_outer_range_independent_results.json` SHA256 `0739cbb1944bdd100e18ca057ca131ac24ec0effa015ac04e5f5b49738e3bbcd`.

48 deterministic seeded independent **complete ideal sumcheck transcript configurations** PASS; each uses fresh whole-ring challenges for ri, sigma,tau,chi,rho,xi and all challenge coordinates of: one outer degree-2 2-variable sumcheck and two inner degree-3 3- and 2-variable sumchecks. Interpolation at public scalar nodes 0..d with exact F13 inverses checks every g_j(0)+g_j(1) and final virtual oracle evaluation; no numerical approximations. Four GP polynomial recursions and root equality also checked. Re-executed twice with identical SHA256. Proof holds for all allowed verifier challenges by CRT-lifted honest per-factor transcripts; sample count is only reproducibility evidence.

**Critical scope:** This replicates the already archived V20 ideal-IOP result, does not authenticate official current PDF, prove a full compiled PCS/Fiat-Shamir vFHE break, verify real 49bit implementation, or supply novel repair. The original manuscript's PDF text extraction around GP Figure1 may drop superscripts; independently verify rendered authoritative edition before any disclosure. **Next V21** official version/rendered-equation authentication; PI controls communication. General I192 remains frozen.


## 30. vFHE V21 — exact V20 false range witness survives CRT PCS authentication and illustrative hash-derived challenges (2026-10-14)

**ONE hypothesis [H-V21, falsified in source-structured compilation model]:** Although V20 ideal composite `Pi_range` accepts an invalid ring coefficient-range witness, the source §2.2 + §5/F.1–F.3 conversion from ring oracle polynomials to binding native CRT-factor polynomial commitments, together with hash-derived challenges, automatically adds a diagonal scalar-digit predicate that prevents an accepting transcript.

**Original paper [FACT]:** Cascudo et al. *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286. Research MCP 52pp mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, `VERSION_UNVERIFIED`. Read p8–9 §2.2 (generic PIOP→argument compiler commits oracles, authenticates queries); pp20–23 §4.3 Eq22, Fig1, Theorem4.8; pp25–26 §5 (ring→field product PC); p50 F.1 (tuple of native field commitments, verifier AND over field evaluations); pp50–51 F.2 (matrix+encoded rows+Merkle column testing/eval); pp51–52 F.3 piecewise RS. None introduces a constraint requiring a ring digit to project to the **same scalar integer digit** in every CRT factor. Binding means binding to a unique R polynomial, which can be invalid for the original table.

**V20 counterexample reused, NOT a new hypothesis:** `R=F13[X]/(X⁴+1)`, nontrivial idempotent `e=7+4X²→(1,0)`, coefficient bound B4, beta4, ellstar3, `vtilde(i)=e` outside coefficient table, `htilde(i,j)=e` at j=(0,0), 0 otherwise. Eq22 is exact, and per-field honest counters CRT-glue into a valid Figure1 inner lookup transcript. All source ideal PIOP checks succeed for arbitrary ring challenges.

**ONE minimal decisive compiled-interface test [EXPERIMENT]:** Local stdlib script `/mnt/data/vfhe_v21_compiler_fs_interface_gate.py` (SHA256 `3501ad0883026396d1497760e7fff1f8a2b22eca65e507fd4f495ad2179f1c97`), deterministic JSON `/mnt/data/vfhe_v21_compiler_fs_interface_results.json` (SHA256 `2bf5355c633e15f77049834c2d4ecdb7499926159ea48fa35a863bb8a7e67736`). Uses V20 script as local dependency. Project **nine** ring oracles (v,h,read,final,table and four GP trees) to both native `F13[u]/(u²-5)`, `F13[u]/(u²-8)`, pad odd MLE arity to even 4, encode 4x4 MLE matrices using the SOURCE SPECIAL CASE of F.3 [N/2=2,N/4=1] piecewise-RS repetition `Enc([a,b,c,d])=[a,a,b,b,c,c,d,d]`. Build SHA256 Merkle trees on encoded 4-vector columns, prove/check openings, and assert F.2 testing `Enc(r·U)|Q=r·Uhat|Q` plus F.2 evaluation `Enc(q1·U)|Q'=q1·Uhat|Q'`, `f(a)=<q1·U,q2>`, and F.1 `Phi_j(f(a))=Phi_j(f)(Phi_j(a))`. For this one toy test Q=Q'=all eight columns (full rather than security sampling). Early v/h/read/final/table field commitments precede `sigma,tau`; four GP commitments made after sigma,tau and before `chi,rho,xi`; all these challenges and sumcheck challenges derived from staged SHA256 roots using an **illustrative** domain-separated FS schedule. All ring grand-product roots, two inner degree3 sumchecks, outer degree2 sumcheck and original false range status checked. Three different public nonces all PASS, **864 authenticated encoded column checks PASS**, mutated Merkle leaf rejected. Deterministic rerun has identical JSON digest.

**Mathematical conclusion [DERIVATION]:** A *faithful* standard oracle→PCS compilation that only proves committed polynomial evaluations cannot strengthen the underlying checked relation `Pi_range`; committing honestly to a ring polynomial `e∉t_beta` that nonetheless satisfies its per-field proof identities is entirely compatible with cryptographic binding. A hash-challenge schedule alone cannot correct a false relation when the demonstrated algebraic identities hold for EVERY verifier challenge. This is source-structured conditional interface evidence, not an exact published deployed compiled SNARK forgery.

**Source-version gate:** Live official ePrint PDF download failed; web search indexed a **different older 50pp** PDF (missing the mirror edition's clarified Theorem4.8 restrictions). Screenshot of that web cached PDF failed. Official Springer CRYPTO2025 paper `10.1007/978-3-032-01907-3_21`, pp643–677, metadata verified but full chapter is institution/subscription gated. Thus no proof that official current/proceedings source contains identical detailed Figure1 and compiler formulas. Complex typography still needs independent visual verification. No author contacted.

**STATUS:** FAIL compiler-alone-adds-diagonal-predicate H-V21 in scoped source-structured toy; PASS exact 864 authenticated checks + hash-derived protocol identities; official-version/real-world exploitation UNCLEAR, HUMAN_REVIEW.

**RESULT:** Integrity of per-field polynomial openings ≠ membership in common scalar digit table. Existing V20 ideal soundness counterexample not eliminated by basic source F.1/F.2 PCS interface or illustrative FS hashing.

**NEXT_ACTION V22:** prioritize **authenticated final full paper** and final Figure1 source, then source-faithful complete compiled proof gate if any implementation actually supports it; otherwise prepare PI-reviewed evidence package without unsupported claims. NO unilateral author outreach, no generic further toy examples.

**STATE_UPDATE:** YES V21 separate track only; old global general I192 remains frozen.

**Local technical report:** `/mnt/data/VFHE_V21_Compiled_PCS_FS_Interface_Gate_2026_10_14.md` SHA256 `dd9cf533401e589183b6fe11511bb0b78e6d8c6ebb2b26b997b4e40ad7bb47f7`.


### V21 source provenance addendum — official 2026 revision timeline (2026-10-14)

**IMPORTANT:** ADDENDUM to an ALREADY COMPLETED V21 round, NOT V22 or a second V21 hypothesis. Existing V21 §30 independently analyzes toy PCS plus illustrative FS (3 transcripts, 864 Merkle-authenticated checks); no claim its hash schedule implements authors' actual complete compiled SNARK. Current independently gathered source-edition/provenance evidence supplements §30 only.

**[FACT, official IACR metadata]** Landing https://eprint.iacr.org/2025/286 (checked 2026-10-14) states history 2026-02-16 revised (initial submission 2025-02-19). The NOTE is "Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements." Publication info "A minor revision of an IACR publication in CRYPTO 2025." Springer official published chapter https://link.springer.com/chapter/10.1007/978-3-032-01907-3_21 first online 2025-08-17, pp643–677; hence the February 2026 revised ePrint postdates the initial CRYPTO published chapter. Neither version can be presumed to contain identical full text.

**[FACT, TWO distinct PDF source renditions]** PDF https://eprint.iacr.org/2025/286.pdf as WEB SEARCH CACHED is a 50-physical-page OLDER rendition with running headers "Authors Suppressed Due to Excessive Length". Its printed theorem 4.8 omits later explicit beta<pmin and 2^ellstar<pmin assumptions, and old Appendix E.2 invokes Lemma4.6 for the whole ring. It is stale web indexed PDF text, NOT current official bytes. Web PDF screenshot attempted pages 21,22,45 but all returned CACHE MISS; therefore no visual authentication was possible.

Research MCP get_eprint_paper(2025/286) cache_hit=true on source_kind github-mirror URL https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf; source_revision a549654c5dffa3484e95e8244056f4a27c48c3e6; 52 pages, 836746 bytes, SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; version_status VERSION_UNVERIFIED. This 52pp version has Theorem4.8 beta<pmin and 2^ellstar<pmin (physical p23) and Remark4.9 (physical p24) explaining a previous faulty invocation of Lemma4.6 over rings and now restricting the lemma to fields. This is STRONG textual indication of the revised version, but NOT SHA-authentication against the official 2026-02-16 PDF. Official all-versions history endpoint returned HTTP403 and direct PDF download failed; no independent official exact binary was obtained.

**[FACT, inspected mirror logic]** Despite revised bounds, Appendix E.2 physical p48 still makes the FALSE inference that an invalid ring scalar-table digit MUST be invalid in at least one projected CRT field. V17 construction e=7+4X²→(1,0) shows rectangular vs diagonal contradiction; V20 parameters beta4<13 and 2^ellstar8<13 comply with the revised theorem restrictions. Qualitative comparison of cached old 50pp Fig1 and 52pp mirror Fig1 extracted TEXT shows common memory counters, GP recursions, two zero-sum checks and final root equality, and no explicit cross-field diagonal predicate; their exact visual/glyph/index equality is UNVERIFIED (MCP formula extraction warns of missing glyphs).

**[RESULT]** PASS official public revision history and proof-fix timing confirmed; PASS 52pp mirror includes new bounds yet contains a separate explicitly invalid CRT-projection inference not excluded by those bounds. UNCLEAR byte identity with 2026-02-16 official revised PDF, visually exact Figure1, Springer chapter content, and actual compiled/FS SNARK impact. The work remains a scoped IDEAL-PIOP/PCS-interface finding, NOT authenticated official/final compiled cryptographic exploit.

**Local evidence summary** /mnt/data/vfhe_v21_source_authentication_gate.json, SHA256 6730b43a97b1be6c72ed589316d5435307045c81c4c56a73c3ee4a556e43fe4d. This JSON truthfully marks visual and official hash verification FALSE and records the exact links and dates. Existing MISSING_SOURCES.md already has an entry for Cascudo ePrint2025/286 official PDF and continues MISSING_CURRENT_OFFICIAL_BINARY; do not mark RESOLVED.

**NEXT_ACTION remains V22 only with PI continuation:** obtain and SHA-authenticate Feb 16 2026 official PDF and publisher version as authorized, visually verify Figure1 and Appendix E.2; only then advance any claim about current published security. No unsanctioned author contact. Global I192 frozen.


## 31. vFHE V22 — official-version and released full range-verifier availability gate (2026-10-14)

**Primary hypothesis H-V22 [one decisive acquisition/code check]:** Authoritative currently released paper plus public author proof-of-concept source suffice to run V20's false coefficient-range witness against the **authors' actual complete compiled Pi_range verifier** and thereby close source/implementation provenance. **STATUS FAIL/SOURCE_BLOCKED** for that availability hypothesis, **NOT** a paper soundness result.

**[FACT, IACR current landing https://eprint.iacr.org/2025/286]:** Received 2025-02-19; revised 2026-02-16, release note explicitly **"Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements."** The record describes a minor revision of CRYPTO2025; formal chapter DOI https://doi.org/10.1007/978-3-032-01907-3_21 pp643–677. SOURCE_CRITICAL: Feb-2026 ePrint revision **postdates** CRYPTO initial chapter and cannot be silently equated to Springer published bytes. Web-indexed PDF is a stale 50pp version; screenshot of web PDF physical p22–23 failed with CACHE MISS; IACR versions endpoint HTTP403; direct official PDF byte download failed. Existing full-text Research MCP mirror has **52pp 836746 bytes**, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, `VERSION_UNVERIFIED`. Its p23 Theorem4.8 and p24 Remark4.9 are consistent with later proof restrictions, but exact hash-equivalence to Feb2026 official is **UNVERIFIED**. Prior V17–V21 are scoped only to this 52pp rendition.

**[FACT, public code gate]:** Connected GitHub plugin retrieved live public `vfhe/proof-friendly-CKKS` repo metadata and actual README, `pyckks/bench_sumcheck.py`, `lib/main_benchmark.cpp`. README explicitly labels reference code **proof-of-concept** and documents only CKKS multiplication benchmark, sumcheck benchmark, piecewise RS coding benchmark. Repo-scoped indexed code searches for `read_ts`, `final_cts`, `FiatShamir`, `Pi_range`, `verifier`, `lookup` returned zero results; existing `bench_sumcheck.py` and C++ RS main are component bench functions, not a full beta/outer range verifier. Repro GitHub commit snapshot advertised in code result file links: `e44d520ae2d6ce05dee088877ebe54f81c029439` (search index reference, not independently authenticated HEAD). Public repo is not evidence that no private/unreleased program exists. **No executable complete author Πrange prover/verifier found.**

**[DECISION]:** Do not misleadingly run V20's invalid witness against a toy PCS and call it an author's real deployed SNARK exploit; V21 already covered that exact model limit. Nor is source-version matching resolved. Cross-CRT soundness concerns remain algebraically substantive under 52pp inspected paper version, but a final official published flaw claim still lacks a verified edition. A complete source-faithful compiled SNARK attack is not demonstrated. **NO author disclosure/contact without human PI.**

**Research deliverable:** `/mnt/data/VFHE_V22_Official_Revision_And_Code_Availability_Gate_2026_10_14.md`; SHA256 `c70a2daf0dcb4b7a15b0cd83371414348b1ac01ea6202e6fa9a5ef86d408113c`.

**END V22:** STATUS=UNCLEAR/HUMAN_REVIEW for final version and compiled protocol, PASS honest revision/code-availability gate and scoped negative feasibility test; no additional same-toy experiments. **NEXT_ACTION V23** obtain author/current Feb2026 PDF exact bytes (or full live formal Pi_range verifier if available), compare source Figure1 and Appendix E.2 before any stronger claim; if inaccessible, PI may evaluate a source-agnostic but nontrivial diagonal-CRT repair with proven overhead, or pivot to another fully source-backed FHE target. **STATE_UPDATE YES** independent V22 only; global general FHE **I192 frozen**.


## 31. vFHE V22 — official-source authenticity gate

Date 2026-10-14. Independent vFHE V22; global FHE I192 frozen. **ONE PRIMARY HYPOTHESIS:** The exact IACR current official 2026-02-16 PDF can be fetched and SHA-pinned against our 52-page GitHub mirror, then its Figure1/Thm4.8/Appendix E.2 visually authenticated. **STATUS: SOURCE_BLOCKED / HUMAN_REVIEW.** No official PDF bytes or PDF hash obtained and no official full-figure visual verification; this is a failed SOURCE acquisition gate, not a negative result on actual cryptographic soundness.

[FACT — OFFICIAL METADATA] https://eprint.iacr.org/2025/286 landing states 2026-02-16 revision with NOTE "Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements." It describes minor revision of CRYPTO2025 IACR publication. Following its See all versions link returned HTTP403. The DOI is 10.1007/978-3-032-01907-3_21; publisher full text not obtained.

[FACT — DOWNLOAD CHECKS] https://eprint.iacr.org/2025/286.pdf in web search is an OLD cached 50-page PDF with older version of Thm4.8. Web PDF screenshots of zero-indexed physical pages 21 and 45 both failed cache-miss/internal error, so official Figure1 typography is NOT visually inspected. Container Python requests to official original and cache-busting PDF failed DNS resolution; dedicated container download also failed. More public/author discovery found no hash-verifiably identical latest official binary. Do not equate a stale web search cache with live IACR revision.

[FACT — RESEARCH MCP CONTROLLED SOURCE] get_eprint_paper(2025/286) reports cache_hit=true, source_kind=github-mirror, 52 physical pages, 836746 bytes, SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, source revision a549654c5dffa3484e95e8244056f4a27c48c3e6, VERSION_UNVERIFIED. Its physical p23 and p24 have explicit beta<p_min and 2^ellstar<p_min assumptions and Remark4.9 about re-scoping Lemma4.6 to fields. Physical p48 Appendix E.2 STILL contains a separate algebraically FALSE inference: invalid R scalar digit implies at least one invalid CRT field digit. V17/V20 CRT e=7+4X²→(1,0), p13,N4,d2, outer B4 beta4 ellstar3 satisfies both corrected assumptions beta4<13 and 8<13, counterexample to the inspected MIRROR. This is NOT a proof current official PDF retains the passage.

[DERIVATION — SCOPE] The ideal PIOP soundness finding in V17–V20 and the source-structured but ILLUSTRATIVE PCS/FS experiment V21 remain valid as scoped against inspected mirror text. We cannot claim a current official/CRYPTO proceedings flaw, real compiled malicious SNARK transcript, or deployed CKKS attack based on this edition mismatch. No author contacted.

[EXPERIMENT/ARTIFACT] Exact structured evidence summary /mnt/data/vfhe_v22_official_source_gate.json SHA256 4a99a0a7e6cf76f8b635ad14abea5addcd77c0d08ddb15c8cf686ba3565769b7; records official_pdf_sha256=null, current_pdf_byte_verified=false, fig1_official_visual_verified=false. No PDF was generated or falsely named as official.

[DECISION] Source gate UNRESOLVED; existing MISSING_SOURCES.md item for current Feb2026 official binary remains MISSING_CURRENT_OFFICIAL_BINARY. V22 completed as SOURCE_BLOCKED/HUMAN_REVIEW; **NEXT V23 ONLY ON PI CONTINUATION:** ideally PI supplies original official current PDF via ordinary browser, exact bytes + download date, then SHA/pagination/visual Fig1/E.2 comparison. If unavailable PI may instead authorize ONE mirror-scoped minimal diagonal-binding repair falsifier, but not a claim against authenticated latest paper. No unilateral author outreach. General FHE I192 remains frozen.


## 32. vFHE V23 — product-closure impossibility for R-polynomial-only diagonal digit repairs (2026-10-14)

**ONE hypothesis [H-V23, FAIL]:** A finite number of additional **conjunctive polynomial identities over the CRT product ring** R_q, allowing arbitrary existential ring-valued witness oracles but NO non-componentwise predicate or common external integer witness, can enforce `h ∈ t_beta^diag={(j,...,j):j∈[0,beta-1]}` instead of rectangular per-factor digit membership.

**Source [FACT, strictly scoped]:** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint 2025/286, 52pp Research MCP Github mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. Source §3.1 CRT split, §4.3 Eq22/Fig1/Theorem4.8, Appendix E.2 p48, §5/F.1–F.3. Official IACR landing records 2026-02-16 revision “Fixed a flaw in the proof of Theorem 4.8,” but official current PDF bytes still NOT retrievable/hashed; open web PDF is OLD indexed 50pp and screenshot failed cache miss. Latest official or Springer identity is NOT asserted. MISSING_SOURCES.md remains open.

**GENERAL EXACT NO-GO [DERIVATION]:** For R=∏_(k=1)^μ F_k (μ≥2), any set
`A={x∈R^n: ∃w∈R^m, P_i(x,w)=0 in R for all i}`
with arbitrary finitely many polynomials P_i ∈ R[x,w] factors **exactly** as `A=∏_k A_k`, where `A_k={x_k: ∃w_k, P_i^(k)(x_k,w_k)=0 for every i}`. Reason: ring operations and an existential R-witness are precisely componentwise field operations and independent component witnesses. Since beta>=2 and beta<min characteristic, `T_diag={(j,...,j):0≤j<beta}` is NOT a CRT Cartesian product (its fieldwise projections each contain digit0 and digit1, yet cross pair (1,0) is forbidden); no A of this form equals T_diag. Therefore unlimited additional polynomial equation gates, including existential auxiliary ring oracles, cannot alone define a common scalar digit. Claim is about **CONJUNCTIONS**, not global disjunctions or explicit non-ring coefficient/integer checks.

**Interactive scope [DERIVATION]:** If the verifier's checks are conjunctive R-polynomial identities with perfect completeness and ring-valued challenges/answers, each pair of honest scalar-digit transcripts can be pasted componentwise using CRT, preserving round ordering and identities for ALL projected challenges. Hash-authenticated polynomial commitments do not automatically check more than equality/evaluation of the pasted ring oracles. This no-go does NOT apply when the verifier explicitly mixes CRT components via coefficient projection, shared integer witness, full-ring equality disjunction, cross-field quotient relation, or some other noncomponentwise predicate.

**ONE exact source-shaped falsifier [EXPERIMENT]:** R=F13[X]/(X⁴+1)≅F_(13²)×F_(13²) via factors (X²−5),(X²−8), beta4. Let e=7+4X², e²=e, Φ(e)=(1,0); e not in scalar digit table {0,1,2,3}. Yet `e(e−1)=0`, `∏_(j=0)^3(e−j)=0`, and with ring auxiliary w=e, conjunction `e²−e=0; w−e=0; ew−w=0` all hold. General polynomial gluing identity `F(e*x1+(1−e)*x0,e*w1+(1−e)*w0)=eF(x1,w1)+(1−e)F(x0,w0)` is exact for any F∈R[x,w]. Python 250 exact random ring-coefficient polynomial sanity tests PASS, along with original idempotent/root/CRT checks. No reliance on randomness for the theorem itself.

**Research filter [CONCLUSION]:** PARK the entire “add only more R_q polynomial identities/ring-local grand product gates” repair class. To genuinely repair diagonal membership, need some deliberately **noncomponentwise binding**: e.g. independently committed one common bounded integer digit and explicit per-prime and per-extension coordinate link proofs, or base-prime-linear coefficient-extraction plus distinct CRT-prime scalar agreement. WARNING: forcing nonconstant X coefficients to 0 alone does not link **different q-primes**. No candidate cost/soundness of such a repair has been proven; previous V13–V16 already warn of costs. Elementary CRT product closure is not itself a novel publishable theorem.

**STATUS:** FAIL H-V23; PASS algebraic no-go within specified model. Actual final official paper, complete compiled SNARK security and a cost-competitive patch all remain HUMAN_REVIEW/UNVERIFIED.

**RESULT:** A class of tempting low-cost fixes is mathematically incapable of enforcing the desired diagonal scalar membership.

**NEXT_ACTION V24 (only on PI continuation):** Pick ONE genuine noncomponentwise shared-index/digit binding mechanism, derive its exact statement and cheapest falsifier (security plus F.1–F.3 PCS/prover/verifier costs), then reject or expand. Keep original Feb2026 official PDF gap separately open; no author contact without human PI.

**STATE_UPDATE:** YES independent V23, global general I192 remains frozen.

**Local full proof:** `/mnt/data/VFHE_V23_CRT_Product_Closure_Nogo_2026_10_14.md` SHA256 `e22ed367bc22850a64ba08cfa9ed1322a78c8d54dd0210b724e1ba8b0c736524`.
**Code:** `/mnt/data/vfhe_v23_crt_polynomial_repair_nogo.py` SHA256 `307be6a14809372e36a40716e35d472f00f0d49a28dabd9b73d7c582fc81bca5`.
**JSON:** `/mnt/data/vfhe_v23_crt_polynomial_repair_nogo_results.json` SHA256 `7b807f210bd5d2be2ded6c4d31381ec36aa647246d656a07ed4b469b174fb774`.


### V23 companion falsifier — X-constant digits still fail across distinct CRT primes (2026-10-14)

**Companion refinement to the existing V23 no-go [FAIL for this separate concrete shortcut]:** Can we fix the 52-page MIRROR's Pi_beta_range / Pi_range diagonal CRT gap with ONE extra condition that every lookup digit h(i) is CONSTANT in the ring polynomial variable X (i.e. coefficients of X^1,...,X^(N−1) vanish), while leaving the original per-CRT-field digit table lookup alone? V20 nonconstant idempotent e=7+4X² would be excluded by this scalarity constraint. V23 tests whether it suffices for coefficient range soundness across multiple source-form CRT primes.

**STATUS: FAIL this natural degree-zero shortcut; PASS exact independent two-native-prime false-range algebraic witness plus deterministic GP identities.** We do NOT falsify all joint integer range/commit-and-prove repairs; we do NOT claim a new flaw in a verified current published version or a fully compiled SNARK exploit. The original V17–V21 mirror-scoped claim is unchanged.

### Source/interface [FACT]

Cascudo et al., CRYPTO2025 *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint 2025/286, cached Research MCP 52pp GitHub mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, VERSION_UNVERIFIED. §3.1 physical p10: native primes p_i=1+(2N/d)*odd, R_q decomposes into product of extension fields F_(p_i^d). §4.3 physical pp20–23: coefficient table T_B in R_q, scalar digit table t_beta={0,...,beta−1}⊂R_q, Eq(22) decomposition and fieldwise lookup Pi_beta_range Fig1. Appendix E.2 p48 makes false inference that ring scalar table nonmembership forces some invalid CRT field projection; V17–V20 cover same-prime nontrivial idempotent. Authors' official revision Feb 2026 exact PDF bytes remain unavailable (V22), so this V23 is MIRROR-model only.

### Counterexample crossing distinct CRT primes [DERIVED]

Choose N=4,d=2, p1=13=1+(2N/d)*3, p2=29=1+(2N/d)*7, q=13·29=377, beta=B=4, c=1, ell=1, nu=2, gamma=0, ellstar=3. Both primes satisfy source odd-multiplier form and theorem beta=4<pmin=13, 2^ellstar=8<pmin. Both native quartic polynomials split into TWO irreducible quadratics: X⁴+1=(X²−z)(X²+z), with ±z both nonsquares (z=5 mod13, z=12 mod29), giving FOUR extension fields total.

Let E=CRT(1 mod13, 0 mod29)=261 mod377, and take the R_q polynomial e(X)=261 with coefficient representation [261,0,0,0]. Then **all X-positive degree coefficients are exactly zero**, satisfying scalar-polynomial/degree-zero repair. Furthermore E²=E mod377, and native CRT extension residues are (1,1,0,0): every native component sees a digit in t4={0,1,2,3}. However e(X) is NOT one of the FOUR canonical INTEGER digits {0,1,2,3} as an R_q element. The TRUE distinction is integer value bounded globally, not polynomial X-degree.

Define outer vtilde(0)=vtilde(1)=e, which VIOLATES the coefficient range table T_4 (constant coefficient=261). Define htilde(i,j)=e if j=(0,0) and 0 for j∈{1,2,3} at each i∈{0,1}. Thus Eq22 vtilde(i)=Σ_(j=0)^3 htilde(i,j)X^j=e exactly and all htilde values are X-CONSTANT (so even scalarity constraints at EVERY digit position pass). Each of the FOUR native fields sees a fully valid table lookup (for p13 the digit e=1, for p29 the digit e=0).

### CRT-glued memory transcript [DERIVED]

Order the 8 h accesses as h=[e,0,0,0,e,0,0,0]. In p13, table counts are final_cts^(13)=(6,2,0,0); in p29, all eight values equal0, so final_cts^(29)=(8,0,0,0). Construct per-prime honest read timestamp arrays by starting all four counters at0 and incrementing on access; they are CRT-combined into ONE ring-valued read_ts oracle with canonical mod377 leaves

    [0,117,118,119,352,237,238,239].

Similarly one ring-valued final_cts oracle has leaves

    [CRT(6,8),CRT(2,0),0,0]
      =[240,145,0,0]
      =[(8−2e) mod377,(2e) mod377,0,0].

Both read_ts and final_cts are fixed BEFORE σ,τ, as source Fig1 requires. In every native prime field/factor the projected full h, read and final represent a HONEST digit-table memory transcript. Consequently for ANY ring σ,τ the source products

    WSh=∏(h+σ(read+1)−τ); RS=∏(h+σ read−τ);
    WSt=∏_j(j−τ); S=∏_j(j+σ final_j−τ)

satisfy WSt·WSh=RS·S as an identity in R_q by CRT. Grand-product proof polynomials built by binary product trees satisfy all Boolean recurrence constraints. Two internal virtual sumcheck zero sums are true because the product-recursion defects are identically zero at all Boolean nodes. Outer Pi_decomp Eq22 equality holds, and its sumcheck target is true as well. This establishes the ideal algebraic Pi_range counterexample for the HYPOTHETICAL scalarity-only patched system. It does NOT implement a full compiled argument/soundness proof.

### Deterministic cheapest verification [EXPERIMENT]

Standalone standard Python:
`/mnt/data/vfhe_v23_scalarity_only_repair_gate.py` SHA256 `0c3f869deb233ff185036efc4c9916653aa1ceecb1ce4ccaf68283d4f84970d4`.
JSON:
`/mnt/data/vfhe_v23_scalarity_only_repair_results.json` SHA256 `27133f8488bf548508809d2854c33e5da816a22557a75629cd10ff1db822e0c6`.
Both created/run in this session, rerun with identical SHA256; local-only artifacts, not repository source. The script exactly checks p13/29 source-form congruences, primality, irreducibility of four quadratic factor polynomials, E idempotence, X-constancy, false global digit membership and outer coefficient range, every prime-factor native digit membership, Eq22, CRT-lifted per-prime read/final counters, all 4 grand-product tree recursions and final product identity for **233** sigma/tau challenge pairs, including **64** pairs with generally nonconstant ring coefficients. Thus native challenge choices not just small scalar integers are tested. Formula holds universally by fieldwise multiset equality; 233 is independent finite corroboration.

### Correction requirement, cost boundary, and decision

**KILL** "force lookup digits to be constant polynomials in X, then existing per-field t_beta lookup enforces global bounded INTEGER digits." It fixes a within-prime factor mismatch but NOT across-distinct-prime CRT residue mismatch; indeed every nonconstant X coefficient can be zero while all prime-field digits are independently legal and non-diagonal.

**Necessary AND sufficient at purely semantic level:** For every h(i), exhibit ONE canonical integer a_i∈[0,beta−1] (injectively represented because beta<min p) such that **every** native field component equals embed_(p_j^d)(a_i). Equivalently after normal-form coefficient-degree-zero proof, the single constant coefficient in Z_q must admit a CANONICAL lift in [0,beta−1] as integer, not just one bounded residue in EACH prime. Enforcing that link in ZK, committing/injectively extracting that a_i before native challenges, obtaining 128bit soundness and competitive cost are all UNPROVED. Re-checking integer range via the same flawed CRT lookup would be circular. Existing general CP/range/equality designs (V12) are prior art, so no standalone novelty claim.

**NEXT_ACTION V24 upon PI continuation:** ONE minimal, source-specific, noncircular **canonical integer witness LINK** design test. Suggested falsifier: Can a range-constrained common bit decomposition for h(i) and its CRT-native values be batched with a single sound postcommit linear identity check, without assuming the native codeword extractor already proves the intended shared integer semantics? Need one explicit binding/extraction interface and bound for a one-coordinate malicious mismatch, not another toy scalarity sample. Or PI may halt until official ePrint PDF revision is supplied. No unsolicited author contact.

**END V23:** STATUS=FAIL naive minimal patch; RESULT exact p13/p29 CRT prime-level counterexample, full source-form Eq22 and honest fieldwise GP constraints; NEXT_TEST noncircular global integer link; STATE_UPDATE=YES independent V-series only; general global I192 frozen.


## 33. vFHE V24 — bounded shared integer MLE-opening repair FAILS the no-wrap/soundness budget (2026-10-14)

**ONE hypothesis H-V24 [FALSIFIED, proposal NOT authors' claim]:** After native fieldwise scalar-digit lookup checks, enforce a COMMON digit vector across distinct CRT prime characteristics using a **few** additional common small-nonnegative-integer MLE evaluation points `r∈{0,...,K−1}^ell*`. Obtain authenticated F.1/F.2 per-field openings `H_j(r mod p_j)`, center-lift them to ordinary integers, and compare lifts. There is **no auxiliary range/quotient proof** of evaluation integers. One decisive test simultaneously asks whether a universally no-wrapping S_K can yield 128-bit soundness against a one-Boolean-position digit mismatch with few direct queries.

**[SOURCE FACT]** Cascudo et al., ePrint2025/286 Research MCP 52pp GitHub-mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. §3.1 p10: prime `p_i=1+(2N/d)*a_i` with odd a_i and N/d native field factors per prime. §4.3 Eq23 pp20–21 small scalar-digit table `t_beta`; p24 quotes **25** PIOP oracle queries; §5/F.1/F.2 native field PCS. This is a **NEW REPAIR IDEA TEST**, not a theorem/error asserted in source. Exact live Feb2026 revised official PDF still missing; no author contact.

**[EXACT SOURCE-COMPATIBLE PARAMETERS]** N=2^14,d=4,ell*=24 (outer ell10,nu14,gamma0),B=beta=4 (b2,c1), two 49-bit primes satisfying source odd-a format:
- p1=562949953216513=1+8192·68719476711;
- p2=562949952987137=1+8192·68719476683.
Both pass deterministic u64 Miller-Rabin, have 49 bits; beta=4 and 2^ell*=2^24 < min prime. No claim of complete CKKS security instantiation.

**[SHARP UNIVERSAL INTEGER NO-WRAP BOUND]** For Boolean-MLE L_b(r) and 0≤digit h_b≤beta−1, sum_b L_b(r)=1. Let A=Σ_b |L_b(r)|=∏_i(|r_i|+|1−r_i|). Max possible |H(r)| over legal nonnegative digit tables is (beta−1)(A+1)/2, and for r∈S_K^ell*: A≤(2K−3)^ell*. At K3, this bound is **423644304723 < min p/2≈281474976493568**, so centered lift is universally exact. At K4, the sharp bound is **89406967163085939 > max p/2**. Indeed common HONEST legal digit array h_b=3 iff #zeros(b) even, 0 otherwise; at r=(3,...,3) the integer MLE is 89406967163085939, whose centered residues are −102075398339628 (p1) and −102075361868844 (p2). This candidate's canonical-lift equality **falsely rejects equal good digits** at K4. S_K for K>4 includes the same bad point. Thus uniform K3 is the largest complete S_K for these parameters under this direct comparison rule.

**[EXACT SINGLE-ERROR SOUNDNESS, THE ONE DECISIVE TEST]** h1=0 at all Boolean indices; h2=1 ONLY at all-one index b=(1,...,1), zero otherwise. Both have legal beta4 digits but are NOT a shared integer vector. Their integer evaluation difference is D(r)=∏_i r_i. For independent uniform r∈{0,1,2}^24, P[detect]=(2/3)^24=5.940319206354905×10^−5, so P[false accept single query]=0.9999405968079365. To drive (1−delta)^t≤2^−128 requires **t=1,493,526** independent whole-ring evaluation points, validated that t−1 fails threshold. This is about 59,741 times the original 25 **ideal ring oracle query** baseline, **NOT** a comparison of actual prover runtimes. F.1's two primes × N/d=4096 factor PCs means up to 8192 native field openings PER extra ring evaluation (unbatched), i.e. 12,234,964,992 native field evaluation instances across all repetitions. Different batching or secure data structures could change this drastically; it is NOT a universal lower bound for all repairs.

**[COMPUTED]** Reproducible pure-stdlib Python script `/mnt/data/vfhe_v24_small_integer_eval_gate.py` SHA256 `98ed3d37a325f9d2732539a228b483a2653176ecf550305cdc858cbc0ca6ec69`; JSON `/mnt/data/vfhe_v24_small_integer_eval_results.json` SHA256 `2e4e815b5ebf3d64c4560fe84b38714d5433ac683f228c99c9758686c6fd20f3`; exactly checks primes, inequalities, honest K4 false rejection, K3 sparse-difference probability/required repetitions, and 100000 seeded trials (7 detections vs expected 5.94). Mathematical conclusions arise from the formula, not Monte Carlo.

**Scope / privacy / novelty:** Direct integer-lift checking may itself reveal private linear combinations; ZK NOT established. No actual full Brakedown/FS compilation or latest-author source proof; no 128-bit attack on deployed vFHE. **PARK** this particular uniform bounded-small-integer direct-opening proposal. It does NOT disprove other noncomponentwise common integer witnesses, quotient/range proofs, batch field comparisons, high-entropy shared challenges or codes. Elementary interpolation / one-position testing is not a publication claim.

**STATUS:** FAIL H-V24 low-cost shortcut; PASS exact no-wrap and soundness falsifier. 
**RESULT:** K3 gives completeness but ~1.49 million checks for 128-bit worst-case target; K4 gives an explicit honest false-rejection. 
**NEXT_ACTION V25 (PI continuation):** one noncircular common-bit/common-integer commitment with high-entropy field challenges and verifiable integer reductions; cheapest falsifier should examine cross-field quotient soundness and F.1/F.2 prover/PCS cost before expansive implementation. If no viable design, HUMAN_REVIEW/pivot. Keep Feb2026 official source missing gate open, no unilateral author disclosure.
**STATE_UPDATE:** YES V24 separate series; global I192 remains frozen.

**Local report:** `/mnt/data/VFHE_V24_Small_Integer_Shared_Evaluation_Cost_Gate_2026_10_14.md` SHA256 `167d69f9e4b4ad35baa89d90490ae2206054cbcc9a0aa37903aaf180e07f1be7`.


### V24 companion privacy falsifier — public native MLE openings expose shared bounded digits

Date 2026-10-14. Independent V24 only; global I192 FROZEN. SOURCE is inspected ePrint2025/286 GitHub mirror 52pp SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; current Feb2026 official binary VERSION_UNVERIFIED.

**ONE PRIMARY HYPOTHESIS [FAIL under a demanded zero-knowledge goal]:** add a perfectly hiding common third-field commitment C to canonical bounded integer digits a_j, then link each native CRT-field MLE h_f by publicly showing random extension-field evaluation points r_f and corresponding y_f=h_f(r_f)=Σ_j a_j chi_j(r_f). Claim that hiding C ensures hiding of a even if native PCS sends these evaluations openly.

**Decisive falsifier [DERIVATION]:** Every such public native MLE opening is a known linear form y_t=Σ_j chi_j(r_t)*a_j in THE SAME unknown a. All factors over the same characteristic p have publicly computable isomorphisms into a common F_(p^d). Convert points/answers to that basis and form matrix M of weights chi_j(r_t). If rank(M)=H=2^ellstar, public y determines a uniquely by exact Gaussian elimination, regardless of how hiding C is. This does NOT require breaking Merkle/Pedersen or the underlying field PCS. It is an information-theoretic transcript leak. H fewer independent public openings need not enable algebraic full recovery; neither privacy failure at all original parameter choices nor vulnerability of the original paper's own stated confidentiality contract is claimed.

**Source compatibility [FACT]:** Original §3.1 physical p10 says p=1+(2N/d)*odd, k=N/d extension factors. Original §4.3 pp20–23 has ellstar=ell+nu+gamma, native R-valued MLE digit h. Original Appendix F.1 p50 splits PCS by CRT factors. F.2 p51 explicitly sends native field vectors v=r*U_f and v'=q1*U_f to verifier and includes claimed evaluation y, with Merkle-column checks; those public values are not rendered ZK merely by appending a new hiding digit commitment. A separate cross-field CP proof is OUR proposed auxiliary construction, absent in the inspected paper.

**One source-form experiment [EXPERIMENT PASS]:** N16,d2,p113=1+(2N/d)*7, k8, beta4, ell1,nu4,gamma0,ellstar5,H32. Checks beta4<p113 and H32<p113. X^16+1 factors exactly as ∏(X²-z_j), z_j=[35,40,42,48,65,71,73,78], all quadratic irreducible; common extension K=F113[T]/(T²−3). Explicit public factors s_j with 3*s_j²=z_j give isomorphism native X -> s_j*T. All evaluation challenges sampled in TRUE full F_(113²)^5, not just base-field scalars. One shared a∈{0,1,2,3}^32. For each of 4 rounds, disclose point and native evaluation in EACH of 8 CRT factors (32 evaluations total); field-isomorphic public coefficient matrix rank after rounds 1..4 is [8,16,24,32]. Exact Gaussian elimination of 32×32 extension-field system recovers every original integer digit, all extension components zero. Every native MLE evaluation reverified independently. Two runs matched SHA256:
script /mnt/data/vfhe_v24_public_mle_leakage_gate.py SHA256 1531c94de5592b80058f2feec4d42e203bfe8af9cbca53ce9ee2c9329823ac27;
JSON /mnt/data/vfhe_v24_public_mle_leakage_results.json SHA256 b93f673edfdf137ab311e0a6dfe8fbe30e1c0425eef31f5276cc0c5e4696bf09.
Full standalone research report /mnt/data/vfhe_v24_research_note.md SHA256 78540f3fe4cf81c36248a43bb242718a4b7218c1a3608f8633f5becdd2ba22ae. Files LOCAL ONLY; no actual proof system, Pedersen group or 128-bit benchmark implemented.

**Conditional soundness gate [DERIVED]:** For FIXED nonzero native MLE difference and true uniform r∈F_(p^d)^ellstar after BOTH commitments are bound, standard Schwartz-Zippel bound Pr[difference(r)=0]≤ellstar/p^d. Toy p113,d2,ellstar5 => 5/12769≈0.000391573 per round, not real cryptographic security. Full native PCS binding plus KNOWLEDGE-SOUND zero-knowledge link from same C-opening a to the native evaluation still required. Generic hidden third-field vector commitment C does not evaluate the MLE across a different characteristic without explicit proof and mod-p quotient constraints (V14). A protocol avoiding public y may evade V24 leakage, but the inspected F.2 interface publicly uses native field v,v' and claimed y, so cannot call a direct append-only patch ZK.

**Decision:** FAIL automatic hiding of naive PUBLIC native MLE evaluation shared-bit-commitment repair. KEEP potential MLE-identity-test soundness only if an independently proven ZK cross-field link conceals sufficient native linear information. NO original paper ZK-violation claim, official Feb2026 exploitation claim or new cryptographic primitive. **POSSIBLE SUBTEST UNDER ALREADY-RECORDED V25:** One minimal masking feasibility falsifier against original F.2, test whether additive blinders can conceal v and v' while preserving Merkle column-code linear checks and claimed y; if not, identify explicit PCS API redesign and compare to established hiding PCS. Do not resume abandoned RAA minor scans. **STATUS FAIL privacy shortcut, PASS exact rank certificate, STATE_UPDATE YES independent V24; I192 frozen.**
