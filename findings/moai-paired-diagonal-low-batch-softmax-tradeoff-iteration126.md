# Iteration 126 — Low-batch paired-diagonal Softmax: one extra rotation can halve nonlinear ciphertext work (local only)

Date: 2026-10-12. PI authorized I126 target selection after I125. ONE primary falsifiable hypothesis and ONE minimal exact plaintext-semantics toy test. New target distinct from PARKED BJ/LEAF/FAB/SPRU/FEFBS branches. No compiled FHE benchmark, no author contact, no paper correctness allegation.

## Original primary source
Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, IACR ePrint **2025/991**, https://eprint.iacr.org/2025/991. Research MCP obtained full **32 physical-page** original PDF from GitHub ePrint mirror; SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, VERSION_UNVERIFIED.
Read §3.1 pp5–6 for column/diagonal packing and matrix products, §3.2 pp6–7 for interleaved batching, §4 Algorithm 1 pp8–9 for rotation-free diagonal Softmax, §5 p10 and Appendix F Algorithm 9 p29 for single denominator bootstrap and Goldschmidt inversion, §6.1 p11 for **256-input amortized** BERT implementation at ring N=2^16, CKKS slot count S=2^15, and Appendices B–C pp18–22 for algorithms 3/4 and batching. Existing I125 state/archive de-dup checked; no direct named MOAI research notes in findings/failures listings. No claim of exhaustive novelty search.

[FACT] Baseline MOAI diagonal Softmax stores m diagonals of an m×m matrix in m distinct CKKS ciphertexts; after slotwise exp, m ciphertexts are added into row-wise denominators, denominator is bootstrapped then inverted once, and each of m exponential ciphertexts is multiplied by its inverse. Full BERT batch B=256 at m=128 saturates S=32768 available slots with B*m=S for each diagonal ciphertext; the original source explicitly emphasizes rotation-free normalization and throughput.

## ONE primary hypothesis / ONE decisive test

[HYPOTHESIS] In low-batch regime where `m*B≤S/2` and even m, grouping pairs of encrypted diagonal vectors into the two halves of a CKKS ciphertext allows correct row-wise Softmax with **one extra global half-rotation** and reduces expensive ciphertext-exp and final ct×ct multiply calls from m to m/2, compared to MOAI's independent-diagonal layout, PROVIDED this paired ciphertext format is already available at the Softmax input.

[FALSIFIER / MINIMAL TEST] Algebraically derive denominator and output in plaintext SIMD, and construct TWO different m=4 matrices with B=2 and S=16 slots to check whether the half-rotation mistakenly mixes row denominators or samples. This is a correctness-and-operation-count test LOCAL TO SOFTMAX, not a full pipeline feasibility test.

## Derivation / deterministic toy verification

Write `H=S/2`. Let each vector `D_j∈R^H` consist of the j-th upper diagonal entries of each of the B matrices (with consistent placement and padding if mB<H); define pair ciphertext plaintext vector:
```
  P_k = [D_{2k} | D_{2k+1}],  k=0,...,m/2−1
```
where vertical bar denotes concatenation of length-H lanes. (For mB<H, padding slots have no output significance; all active row positions must be aligned.)

Evaluate the same slotwise exp polynomial f for every pair, then
```
  U = Σ_k f(P_k) = [E_even | E_odd],
  T = U + Rot_H(U) = [E_even+E_odd | E_even+E_odd] = [Z | Z]
```
with `Z_i=Σ_{j=0}^{m−1} f(A_{i,i+j})` (indices modulo m) for each sample and each row. With ideal `f=exp`, `Z_i` is exactly that matrix row's Softmax denominator. Apply one bootstrap if necessary and slotwise inverse (same as MOAI), then each `f(P_k) ⊙ (1/T)` contains normalized diagonal 2k and 2k+1 in aligned halves, and requires only m/2 ciphertext multiplications. The extra rotation `Rot_H` permutes the *two halves* of the entire S-slot ciphertext. No rotations inside the m×m matrices are needed in this LOCAL Softmax stage.

Exact public scratch check performed using rational arithmetic, no ciphertexts:
```
m=4; S=16; B=2; H=8
exp(A^(0))=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
exp(A^(1))=[[2,5,1,3],[4,2,7,1],[8,1,2,3],[3,6,4,2]]
D_j = concat over sample r and row i of exp(A^(r)_{i,(i+j) mod m})
P_0=[D_0|D_1]; P_1=[D_2|D_3].
U=P_0+P_1; T=U+Rot_8(U).
T = [10,26,42,58,11,14,14,15 | 10,26,42,58,11,14,14,15].
For both paired ciphertexts, P_k/T gives EXACT original diagonal-packed Softmax rational elements, including sample0 first row [1/10,1/5,3/10,2/5] once reconstructed. Python Fraction equality tests PASS at every position.
```
Thus `row-denominator mixing falsifier` did not occur.

## Operation-count trade-off and hard scope gate

For one set of B inputs, with paired input already available:
- Baseline MOAI: m exponent-polynomial ciphertext evaluations, m final ciphertext×ciphertext multiplications, one bootstrapped denominator/inverse, **zero** denominator rotations.
- Pair layout: m/2 exponent-polynomial ciphertext evaluations, m/2 final ciphertext×ciphertext multiplications, one bootstrapped denominator/inverse, **one** half-slot automorphism and sum.
- Per-ciphertext multiplicative depth remains unchanged; actual CKKS precision/noise and machine performance NOT checked. Additional half-rotation requires a Galois key and adds key-switch noise.
- Capacity: `B≤S/(2m)`. At N=2^16, S=32768,m=128: `B≤128`. The published MOAI end-to-end BERT evaluation uses B=256; for that full batch, the proposed layout needs at least two waves and **the total numbers of nonlinear ciphertext evaluations and output ciphertext products return to baseline levels** while adding rotations. NO claim of improvement over full-batch results.
- Crucial untested boundary: MOAI upstream Algorithm 3 outputs m *independent* diag ciphertexts with a specific interleaved layout; combining them online into m/2 two-lane ciphertexts can itself need plaintext masking, slot permutation/rotation, additions, rescale/level and new keys. Likewise downstream Algorithm 4 expects separate diagonals. A naive repack/unpack may cost Ω(m) rotations/masks, erasing local savings. Possible future benefit would require a new **native paired-diagonal matrix multiplication representation** through both neighbors, not merely a local Softmax trick. No such end-to-end construction/benchmark is demonstrated.
- Prior-art risk: SIMD packing/half-slot summation is standard FHE functionality and MOAI already employs interleaved packing across many inputs. Local identity itself has LOW novelty. `NOVELTY NOT VERIFIED`.

## End of iteration
STATUS: **PASS LOCAL PLAINTEXT CORRECTNESS / UNCLEAR FHE-END-TO-END / HUMAN_REVIEW**.
RESULT: A 2-lane diagonal packing with one half-rotation achieves correct local Softmax for even m at low batch and can halve exponent and final ciphertext-product call counts, but sacrifices batch capacity by 2; all full-pipeline transition, noise, latency/key-size and originality claims unresolved.
NEXT_ACTION: PI decides whether to authorize ONE decisive pipeline cost falsifier in I127: take MOAI Appendix B Algorithm 3 output and Appendix B Algorithm 4 input, derive minimum pair pack/unpack operation counts (rotations, masks, levels, key switches) for m=128, B=1 and compare against saved Softmax exponent/multiply work. If repacking costs negate savings or output format cannot be maintained, PARK. No implementation until cheaper algebra/cost test passes. Otherwise PI may choose another new target.
STATE_UPDATE: YES, new bounded correctness and cost-regime observation, with clear caveats; not an established scientific contribution.
