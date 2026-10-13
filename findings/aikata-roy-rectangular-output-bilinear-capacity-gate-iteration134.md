# Iteration 134 — Rectangular HE matmul: an explicit-output bilinear-capacity lower bound missing from a proposed k p² packing model

Date: 2026-10-13. PI authorized I134, after I133 recommendation to PARK MOAI I126–133 and move to a new structural FHE matrix-work target. ONE primary falsifiable hypothesis and ONE smallest bilinear-dimension/rank test. No author contact/disclosure, no encryption/implementation. Independent of but intellectually related to archived Iteration 38 `failures/ckl-rectangular-cpmm-missing-output-block-factor.md`; not a novel bilinear-rank theorem.

## Original paper / provenance

Aikata Aikata and Sujoy Sinha Roy, *Secure and Efficient Outsourced Matrix Multiplication with Homomorphic Encryption*, INDOCRYPT 2024, IACR ePrint **2024/1730**, https://eprint.iacr.org/2024/1730. Original full **25 physical-page PDF** acquired via Research MCP from fixed GitHub ePrint mirror (cache hit), PDF SHA256 `69847d0bdffe3bd148b1f9bd76278057aa24cfa02f1aab8e8c2e9ac80820a412`, source revision `f5d3cf62f785d517fc2ebbcc09d8fc09b99d4113`, latest version `VERSION_UNVERIFIED`.
Primary evidence:
- §3.3 physical pp14–16, generalized Algorithm 4: for square dimension d and s matrix copies per ciphertext, ciphertext×ciphertext multiply count d/s, and maximum packing d³ at s=d has ONE Ct×Ct call with linear slotwise preprocessing/postprocessing.
- §4.1 physical pp17–18: rectangular zero-padding strategy with k=max(ℓ,d,t) potentially requiring k³ slots.
- **§4.2 physical pp18–19:** proposes common divide-and-conquer rectangular generalization A_{ℓ×d} B_{d×t}; text states **packing requirement k p²**, k=max(ℓ,d,t), p=min(ℓ,d,t), after discussing illustrations ℓ=4,d=2,t=6 (24 slots) and ℓ=t=2,d=4 (16 slots). States *“After the initial duplication, all the p × p matrices are packed in one ciphertext”* and *“There is no increase in ct-ct multiplications throughout this process, and the multiplicative depth remains at two.”* No complete rectangular implementation/accuracy results: §5 p19 notes divide-and-conquer results can be extrapolated from square benchmarks, with §5 Table4 pp19–20 primarily square/padding sizes. We do NOT claim independent verification of the authors' artifact code.
- Official ePrint metadata page identifies authors and INDOCRYPT2024: https://eprint.iacr.org/2024/1730.

## ONE primary hypothesis / failure condition

[HYPOTHESIS] Under the paper's **standard one-complex-scalar-per-slot explicit row-encoded output** and linear SIMD preparation / pointwise Ct×Ct product / linear postprocessing model, the §4.2 general packing S=k p² can be paired with **one** Ct×Ct SIMD multiplication to materialize **every** entry of C=A B for arbitrary rectangular dimensions, without counting extra output-block multiplicative work.

[FALSIFIER/ONE TEST] Choose **ℓ=8,d=2,t=8** (all powers of two; CKKS S=32 is a legal slot count). Derive exact linear span dimension of bilinear output coordinate polynomials C_ij, compare against capacity S per sole ciphertext pointwise multiplication, and construct two 8×2,2×8 public matrices with 64 independently indexed output positions. If dim(span{C_ij})>S, no linear rotation/masking after one Ct×Ct SIMD multiplication can give all entries explicitly in standard packed format. This is a precise format+operation-model falsification, NOT a universal FHE lower bound or exploit.

## Derivation

Paper's §4.2 formula gives
```
k=max(8,2,8)=8; p=min(8,2,8)=2; S=k p²=32.
AB has ℓt=64 scalar entries, requiring ≥64 slots if one row_enc ciphertext must contain all entries.
```
Even if the 64 entries are split across ≥2 output ciphertexts, the **bilinear** lower bound remains for a single 32-slot Ct×Ct product followed only by rotations, additions, constant/plaintext masks and other linear operations.

Let `f_ij(A,B)=C_ij=Σ_{r=0}^{1} A_{ir}B_{rj}`. In the vector space of bilinear polynomials over a field characteristic0, the 64 `f_ij` are linearly independent: the monomial `A_{i0} B_{0j}` occurs with coefficient one uniquely in `f_ij`, not in any other `f_i'j'`. Hence
```
 dim span{f_ij : 0≤i,j<8} =64.
```
Any single SIMD Ct×Ct multiplication with S=32 slots creates at most 32 bilinear coordinate functions, each of the form `L_s(A)*M_s(B)` after **separate linear preprocessing of A and B**. Subsequent ordinary CKKS slot permutations, plaintext masking/multiplications by publicly fixed constants, ciphertext addition and replication are linear maps on that 32-dimensional bilinear-output span; hence they cannot produce all 64 linearly independent required output forms. General lower bound in THIS model:
```
 #CtCt >= ceil(ℓt/S).
```
At ℓ=t=n, inner d fixed, p=d, k=n, source S=n d²:
```
 #CtCt >= ceil(n²/(n d²)) = ceil(n/d²).
```
So the missing output-block factor can grow asymptotically when n≫d²; it is not merely a log-rounding irregularity. The simple **output-storage** lower bound and the **bilinear-span** lower bound must be distinguished: extra output ciphertexts alone cannot create new bilinear coordinates from just one Ct×Ct operation under this operator model.

Local minimal exact check: construct formal rank matrix of 64 output coordinate coefficient vectors in a 128-dimensional monomial basis indexed by `A_{ir}B_{rj}`; NumPy real rank equals 64. A separate concrete test with A_i=[i+1,1], B_{0j}=1, B_{1j}=100(j+1) (i,j 0…7) gives 64 pairwise distinct C_ij=(i+1)+100(j+1), demonstrating a single 32-slot row_enc output cannot hold the entire matrix in the ordinary layout. The formal bilinear independence (not numerical distinctness) is the rigorous circuit obstruction.

## Source-scope judgment and important caveats

[DERIVED/NEGATIVE] The unrestricted triple `S=k p²` + **one pointwise SIMD Ct×Ct product** + **full explicit ℓ×t output** fails at ℓ=t=8,d=2. The paper's illustrated ℓ=4,d=2,t=6 case has ℓt=k p²=24, so it does NOT expose the gap. The source §4.2 statement *“no increase in ct-ct multiplications”* may be intended relative to some different number of square-p×p subproblems, or it may implicitly permit multiple output ciphertexts/products; the extracted §4.2 text does not unambiguously resolve that. DO NOT flatly accuse the authors of a proved correctness bug or deny their square-matrix algorithm/benchmarks.

To be explicit, the lower bound assumes:
1. all ℓt complex output entries must be **materialized** in a standard row-wise SIMD representation, not held as low-rank factors or a lazy compressed matrix representation;
2. ciphertext-ciphertext multiplication is an S-slot componentwise Hadamard multiplication of A-dependent and B-dependent linearly preprocessed ciphertexts;
3. after these bilinear products only **linear** operations are used (rotation, masking by public fixed plaintext, addition, modswitch/rescale as approximate linear changes);
4. no alternative special matrix-native plaintext/ring multiplication primitive and no exotic complex conjugation/real-versus-complex subslot optimization is presumed.

If outputs are retained as low-rank factors, a single ciphertext need not explicitly encode all lt values; but the computational task/output interface changes and downstream standard row_enc multiplication would still need a conversion/cost accounting. If the implementation already uses ≥ceil(ℓt/S) Ct×Ct calls, **no contradiction**; this note identifies a proof/complexity **qualification or reporting requirement**, not an active exploit.

[NOVELTY] The linear span/tensor-rank argument is established algebra, and archived I38 CKL 2025/1957 independently found a different missing output-block factor for rectangular CPMM, although its main abstract already accounted for it. **No publishable new construction or verified proof gap yet**. Importance depends on demonstrating that the specific §4.2 implementation truly claims constant Ct×Ct for an output interface that requires explicit entries, or on designing a nontrivial representation/output-block repair with a favorable cost frontier.

## End of iteration

STATUS: **FAIL unrestricted one-product explicit-output compatibility / PASS source-anchored bilinear capacity bound / HUMAN_REVIEW**.
RESULT: In standard row-encoded SIMD rectangular matmul, S=k p² alone is insufficient for one-call full-output realization whenever ℓt>S. For ℓ=t=8,d=2, S32 but rank64 bilinear outputs require ≥2 Ct×Ct products even if they are emitted across multiple output ciphertexts. A source-text ambiguity remains about whether paper §4.2 implicitly permits such extra output blocks; no authors' actual correctness bug or verified novelty asserted.
NEXT_ACTION: PI authorizes ONE next falsifiable check: inspect source artifact implementation or §4.2's exact input-output interface for ℓ=t=8,d=2 and determine whether output blocks are actually counted, then quantify the corrected rectangular Ct×Ct and rotation cost (and whether a nontrivial faster layout remains). If source already counts this factor, PARK immediately. Alternatively pivot to another stronger FHE target.
STATE_UPDATE: YES — new source-specific quantified constraint relevant to the explicit rectangular generalization; avoid making it a proven paper bug.
