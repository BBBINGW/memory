# Iteration 137 — Independent four-point Brakedown evaluation cannot be rank-one-folded into one unchanged F.2 phase

**Date:** 2026-10-13. **PI authorization:** “好的，请继续” after I136. **ONE hypothesis / ONE cheapest finite-field matrix-rank falsifier.** User PI approves final research choices. No code benchmark, actual PCS security test, FHE ciphertext or author disclosure.

## Read before write / why distinct from prior work

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (last I136 SHA `220a8ba28e621ff560e68d0b5b8099bb2660e9f7`), `findings/OPEN_RESEARCH_BRANCHES.md`, `failures/vfhe-shared-brakedown-q2-challenge-fourfold-soundness-iteration136.md`, `findings/vfhe-fourfold-scalar-sumcheck-amplification-cost-iteration94.md`, and I86 `findings/vfhe-public-aggregate-vs-mle-evaluation-rank-obstruction-iteration86.md`.
- Primary paper Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, https://eprint.iacr.org/2025/286. Full **52-physical-page** Research MCP GitHub-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** relative to latest official edition. Re-read **§5 p25–26** and Appendix **F.2 p51**. §5 defines for even ell, m_B=2^{ell/2} and MLE coefficient/evaluation matrix `U_f∈F^{m_B×m_B}`, `f(a)=q1(a)^T U_f q2(a)`; each qj is a length-m_B Kronecker product of `[a_i,1−a_i]` for its corresponding half of the variables. F.2 evaluation phase sends **entire** `v'=q1(a)^T U_f` and verifies `f(a)=v'·q2(a)`, plus code/column-opening consistency. Source allows reuse of TESTING phase across multiple evaluations but does NOT claim a batched EVALUATION phase.
- I136 excluded sharing q2 or last Sumcheck challenge because false sumcheck correlated errors produce only 1/p instead of 1/p^4. I137 **retains fully different/independent terminal points** and tests rank obstruction to using ONE UNMODIFIED F.2 vector opening for a batched claim. It is related to the classical rank-one MLE evaluation observation of **I86**, but here specifically addresses the double-sided matrix `U_f`, 4 distinct terminal MLE queries, and source F.2 communication budget; this is not new tensor-rank mathematics.

## ONE hypothesis and precise falsifier

[HYPOTHESIS] With **four separately independently sampled terminal query points** `a_j`, the proposed I94 fourfold masked aggregate sumcheck can transmit/validate a random linear combination `Y=Σ_{j=1}^4 λ_j f(a_j)` using **one** F.2-style evaluation vector `v_*=u^T U_f` and one right projection `v_*·v`, rather than four evaluation vectors, *while leaving the terminal queries independent and the source's original PCS proof interface unchanged*.

This requires, for EVERY committed `U_f`, an equality
```
 Σ_j λ_j q1(a_j)^T U_f q2(a_j) = u^T U_f v.
```
Equivalently,
```
 M:=Σ_j λ_j q1(a_j) q2(a_j)^T = u v^T,
```
hence **rank(M) ≤ 1**. If a legal 4-point transcript has **rank(M)=4** over one native field, the HYPOTHESIS is false for the unmodified interface. Generalization: any sum of k standard F.2-style rank-one openings has coefficient matrix rank ≤k, so this family of rank-r batched linear functionals needs ≥r such terms. This is a lower bound **ONLY FOR THIS F.2 RANK-ONE LINEAR-FOLDING OPERATOR MODEL**, not a universal PCS communication lower bound. Novel PCS protocols can prove higher-rank linear functionals by other means.

## ONE exact minimal test (four-variable MLE, F29)

Take field p=29, ell=4, m_B=2^(ell/2)=4, standard source `q(x,y)=[x y, x(1−y), (1−x)y, (1−x)(1−y)]` (coordinate basis may be permuted; rank invariant). Independently chosen legal scalar query values in `F29^4` (sample deterministic 4 possible values with no shared mandated challenge):
```
a1=(2,3,7,8)
a2=(2,5,7,11)
a3=(4,3,13,8)
a4=(4,5,13,11)
λ =(1,2,3,4).
```
Define 4×4 matrices `L` and `R` with rows `q(a_j[0:2])` and `q(a_j[2:4])` respectively. Exact integer determinant before modular reduction:
```
 det(L)=16, det(R)=324,
 det(M)=det(L^T diag(λ) R)=16·324·(1·2·3·4)=124416 ≡ 6 (mod29) ≠ 0.
```
The exact M mod29 is
```
 [ 8  0  7 11
   4 17 23 22
  28 26  6 14
  10 19 12  6 ].
```
**rank_F29(M)=4**, so M≠u v^T for any length-4 vectors u,v; not even three rank-one F.2 terms can represent it. Since the determinant is a nonzero polynomial in the points and λ, generic configurations over sufficiently large fields also have rank4. The integer determinant's primes dividing 124416 are much smaller than source's 49-bit field characteristic, so the same example remains rank4 over source-size prime fields, with distinct legal scalar coordinates; source field F_{p^4} also contains these base-field points. This is a rank-scope counterexample, NOT an attack on independent sampling.

Numerical check on a fixed arbitrary integer mod29 matrix
```
U=[[11,16,21,26],[14,26,9,21],[17,7,26,16],[20,17,14,11]]
```
y_j=q1_j^T U q2_j=[1,24,2,16] mod29;
`Σ λ_j y_j ≡3 mod29`, matching `⟨M,U⟩_F≡3`. The rank result is valid FOR ALL U, not only this sanity example. Derived/tested using exact modular Gaussian elimination and independent exact SymPy integer determinant, no floats.

## Communication and security consequences

- **[NEGATIVE]** Four independent general evaluations cannot, in general, be coalesced into one (or 2–3) of the **original** F.2 rank-one dot-product evaluation vectors while preserving the original evaluation functional for every U. Four source-style evaluation vectors `q1_j^T U` are needed by this *literal linear folding family*. This is a **conditional rank-model** vector-count bound only: do not overclaim information-theoretic 4m symbols across arbitrary new proofs, or imply authors intended to do this.
- **[SOURCE COST]** Each original F.2 eval sends an m_B-symbol vector over F_{p^4} per CRT field component, with ~49-bit base p => at least 25 bytes/extension-field symbol as a fixed-length, uncompressed representation. Four such vectors across μ=6144 fields with m_B256 cost 4·6144·256·25 bytes = **150 MiB**; for μ=8192, m_B1024, **800 MiB**. Both are I94 CONDITIONAL layout scenarios because original per-digit c=5 packing and field counts unresolved; they exclude Merkle column proofs and compressed alternative representations. No 4→1 raw-vector communication factor arises under the source F.2 rank-one interface.
- **[SECURITY]** This test is at the *algebraic correctness/cost interface* stage and does not prove an FS/PCS knowledge-soundness theorem. Even if a new arbitrary-rank batched opening PCS is designed, it must keep independent I94 rho and r coordinates, adapt ring/CRT μ-component commitments and prove evaluation binding/privacy/source-scale proof size. The source's existing F.2 testing-phase reuse and potential shared **Merkle column indices** are orthogonal, and may save column authentication bytes but DO NOT compress four independent q1_j U vectors by themselves.
- **[NOVELTY]** Bilinear rank-one-vs-rank-four flattening is elementary linear algebra and conceptually overlaps I86's MLE tensor-rank obstruction. Important cheap design-filter for I137, **not a publishable lower bound**, not a source flaw, and not general impossibility of batched PCS.

## End of iteration

**STATUS:** FAIL one-source-F.2-vector independent-four-point linear folding / PASS exact rank4 counterexample / HUMAN_REVIEW.
**RESULT:** For four distinct legal MLE evaluation points, independent challenges permit a rank-4 coefficient matrix `M=Σλ q1 q2ᵀ`. Under unmodified Brakedown F.2 phase `f(a)=uᵀ U v`, no one-vector (or ≤3 rank-one-vector) fold can express the aggregate for all U. Source-cost reduction 4→1 by linear folding unavailable, and base 150–800MiB conditional four-vector data persists under that exact interface. No actual SNARK forgery, encrypted test or new PCS.
**NEXT_ACTION:** I138 only with PI authorization: optional *different* single falsifiable hypothetical PCS: can **sharing Merkle column openings Q' across distinct independent evaluation points** preserve per-eval binding and reduce any substantial portion of actual proof size, given four uncompressible m_B vectors? Test one precise conditional communication inequality, and PARK if maximal shared-column savings still fall well short of meaningful 10×. Alternatively pivot from vFHE micro-repair to MRFHE or another structural target. Never re-run sharing q2/last challenge, native I88–95 repair, or this rank-one-fold shortcut.
**STATE_UPDATE:** YES — I136 randomness constraint plus I137 rank-four obstruction jointly narrow cheap batched PCS routes, enough to update vFHE branch's future gate.
