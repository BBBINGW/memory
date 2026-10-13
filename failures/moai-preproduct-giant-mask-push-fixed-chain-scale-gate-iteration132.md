# Iteration 132 — Giant half-wise mask push is algebraically correct, but cannot be no-extra-level with full-scale masks on MOAI's unchanged 46-bit CKKS prime chain

Checkpoint: 2026-10-13. PI authorized I132 with “好的，请继续” after I131. Exactly ONE primary claim and ONE algebra+scale-DAG falsifier, with a small exact plaintext verification. No cryptographic implementation and no author contact.

## Read-before-write / provenance

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, and current `STATE.md` after I131 (SHA `6e68231f8500a405a1f496553ca130549b501918`), plus I130 `findings/moai-native-paired-bsgs-halfwise-rotation-cost-iteration130.md` (SHA `3f9c122def303f70aa12e99754b2136a2499fed8`) and I131 `failures/moai-ckks-halfwise-mask-scale1-precision-gate-iteration131.md` (SHA `03ace83686fd00aaa0e3312c1b5c7dbeb7acab53`).
- Original MOAI by Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ICLR 2026 / IACR ePrint 2025/991, https://eprint.iacr.org/2025/991, previously acquired *full* 32-physical-page PDF mirror SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, original latest version VERSION_UNVERIFIED. **Re-read primary physical pp10–11**, §6 reports CKKS scale `2^46`, ring N=2^16, original CPU backend Microsoft SEAL; Appendix B Algorithm 4 p20 and Eq.(3) p18 are the original BSGS comparator.
- CKKS source evidence: Microsoft SEAL `native/examples/5_ckks_basics.cpp` https://github.com/microsoft/SEAL/blob/main/native/examples/5_ckks_basics.cpp explains plaintext/ciphertext scales multiply and rescaling divides by one prime; `native/src/seal/modulus.h` https://github.com/microsoft/SEAL/blob/main/native/src/seal/modulus.h documents **at most 60-bit** bit-sizes for user coeff_modulus primes in `CoeffModulus::Create`; `native/src/seal/util/rns.cpp` also explicitly notes 60-bit user primes; OpenFHE forum https://openfhe.discourse.group/t/masking-without-rescaling/1013 states nonconstant CKKS bitmask vectors must be approximately encoded and normally rescaled, unlike small integer-coefficient monomials.

## ONE primary hypothesis and decisive falsifier

[HYPOTHESIS] Moving I130's **post-Ct×Ct** giant half-wise boundary mask to the V/baby-step operand **before multiplication**, while retaining the same 4096 paired Ct×Ct products and BSGS hoisting, permits accurate full-scale `Δ_M=Δ=2^46` CKKS masks and returns output at the original scale `Δ` with **no additional rescale level and no change to MOAI's existing ≈Δ-bit rescale prime chain**.

[FALSIFIER / CHEAPEST TEST] Derive an explicit commuting/slot permutation identity for the move and verify at m=8 with two genuinely distinct halves, then track all ciphertext/plaintext scales and the necessary single-prime rescale q for the *actual* Δ=2^46 and matched-precision mask Δ_M=2^46. A required single prime `log₂ q ≈92` beyond the 60-bit user-prime bound, or mismatch after the old q≈2^46, kills the claimed same-parameters/no-extra-level shortcut. Include operation counts to avoid hiding lost BSGS reuse.

## Exact algebraic mask relocation

Let S=2H slots, `R_a` = full cyclic left shift by a, `T_a` = independent left shift in each half. Define `U_a=R_{-a}∘T_a`; for 0<a<H, U_a **only swaps the first a slots of the two halves**, leaving other slots alone. This is
```
  U_a(B) = B + F_a⊙(R_H(B)−B),
```
where F_a is 1 on the **first** a positions of each half (not I130's last-a J mask), 0 elsewhere.

Since T is a permutation, it preserves Hadamard product:
```
  T_a( T_{-a}(C) ⊙ B )
  = R_a( R_{-a}(C) ⊙ U_a(B) ).     (★)
```
Proof: use `T_a(X⊙Y)=T_a X ⊙ T_a Y`, and R_a inverse composition. This is exact under ideal SIMD plaintext semantics for each BSGS summand and preserves one Ct×Ct per paired diagonal.

I130 baby `B_r(v)=M0⊙A_r+M1⊙E_r` with `A_r=R_{2rL}D(v)`, `E_r=R_{(2r+1)L}D(v)`, `D(v)=[v|v]` and half-selector `M1`. Then `U_a B_r=A_r+P_a⊙(E_r−A_r)`, where P_a is 1 on the FIRST a slots of the low half and LAST H−a slots of the high half, 0 elsewhere. P_a depends on the giant step α (a=2αtL). Thus the **underlying rotations** A_r,E_r remain reusable across α, but the **masked baby ciphertext itself is no longer shareable across α**.

At m128, 64 pair ciphertexts, t8, g8, dv64, exact schematic operations for this particular push:
```
                              I130 paired BSGS   I132 pushed-mask
Ct×Ct multiplication                 4096              4096
ordinary global rotations            2032              1528
Ct×Pt boundary masks                 1016              4096
nominal KS (ctct+rot)                 6128              5624
```
I132 rotations = hoisted pre-C `n_p−t=56` plus dv per-output `(2t−1)+(g−1)+1=23` = 1528. Each αr output requires one α-specific P_a selector, total n_p dv=4096 masks. The original BSGS baseline remains Ct×Ct 8192, rotations1460, nominal KS9652. This is a **rotation→mask trade-off**, not a free mask removal. Because BSGS pre-rotating C is now ordinary R_-a rather than T_-a, the hoisted C-side masks are gone, and post-product giant masks are also gone; their cost migrates to α-dependent V-side masks.

**ONE exact toy validation:** m8,S32,H16,L2,t2,g2, B=2 distinct matrices, d=dv=3, normalized `C_{ij}=(1+(QK^T)_{ij}²)/Σ_ℓ(1+(QK^T)_{iℓ}²)` from I130. Implement exact `U_a` (first-a-half swap), global rotations, BSGS and dense C·V as Python `Fraction`. All output entries for all rows/columns/samples, and BOTH destination halves, match. Test `(★)` across all a on arbitrary distinct-half vectors for S16/32/64. First sample first row output: [191/197,263/197,452/197]. PASS exact algebra. NO encrypted CKKS code.

## Decisive CKKS level/scale DAG

Assume C-side paired encryption `ct_C` at **scale Δ**, and unmasked baby ciphertexts A,E at scale Δ. Encode desired nonconstant selector P_a at plaintext scale `Δ_M`. For the masked baby:
```
  B'_a = Δ_M*A + EncPlain(P_a;scale Δ_M)*(E−A).
```
The first term uses *exact integer scalar* Δ_M to align scale (does not itself encode a nonconstant selection vector). Both summands are at effective ciphertext scale ΔΔ_M; the plaintext slot content represented is correctly the desired mask-weighted B'_a, assuming mask accuracy.

Then **one** Ct×Ct with C-side scale Δ produces output at `Δ² Δ_M`. Requiring *one* rescale back to Δ means
```
  q_rescale ≈ Δ·Δ_M.
```
MOAI specifies `Δ=2^46` (physical p11). Choosing the usual full-precision mask `Δ_M=Δ=2^46` yields required `q_rescale≈2^92`. **This cannot be a single SEAL user coefficient prime (≤60 bits).** If instead use MOAI-like existing q≈Δ≈2^46, after ONE rescale output scale is `Δ·Δ_M≈2^92`, not Δ; merely editing the scale metadata does not fix actual plaintext semantics. Additional rescale or altered modulus design is required.

General budget with 60-bit single prime and Δ=2^46:
```
  log₂ Δ_M ≤ 14 bits (approx, with headroom).
```
E.g. mask Δ_M=2^12 could be paired with a re-designed ~58-bit prime and one rescale, mathematically; **no demonstration** that such a 12-bit-scale sharp mask maintains enough precision at N=2^16 for full MOAI attention, or that runtime/noise/security/remaining total Q are acceptable. With Δ_M=2^16 the required ≈62-bit prime is still over SEAL's 60-bit prime cap. At equal-scale Δ_M=Δ=2^46 the constraint is decisively violated. Ordinary high-precision mask rescale workflows may use >1 modulus prime and extra level; the general problem is NOT proven impossible.

Important: The `92-bit` number is a **rescale-prime requirement for this specific fused one-level schedule**, not a claim that total ciphertext modulus or runtime must be 92 bits, nor a universal bit-size lower bound for all CKKS algorithms. Alternative scale propagation, pre-rescaling V, lower-precision masks, and bootstrapping/rescale trade-offs are OUTSIDE this I132 primary hypothesis.

## Scientific judgment

[NEGATIVE] Original matched-mask-scale/same-prime-chain/no-extra-level I132 HYPOTHESIS FAILS. [PASS] Algebraic mask relocation / two-matrix rational correctness and explicit operation counts. [OPEN] Reduced mask scale (κ≤14) with enlarged 46+κ bit prime **might** trade sufficient accuracy for same one-level rescale; actual MOAI full N=2^16 accuracy remains unverified, and the required α-specific 4096 masks may overwhelm speed. Full batch B256 still out of one-wave paired capacity. Source MOAI is not incorrect, no actual FHE ciphertext exploit/bug, nothing publishable just from this known CKKS scaling issue.

## Iteration end

STATUS: **FAIL equal-precision fixed-prime one-level mask push / PASS exact algebra and cost counting / HUMAN_REVIEW**.
RESULT: The giant post-Ct×Ct boundary mask can be pushed to a per-giant masked baby ciphertext, preserving one paired multiplication and reducing ordinary rotations 2032→1528, but increasing masks 1016→4096. At Δ_M=Δ=2^46, single-rescale-to-Δ requires q≈2^92, outside SEAL's max 60-bit user primes, so the proposed no-extra-level SAME-CHAIN shortcut does not work. Not a general impossibility for CKKS schemes.
NEXT_ACTION: PI gate before I133. Either (A) ONE crucial *MOAI-sized* N=2^16 precision falsifier for κ≤14-bit reduced-scale half boundary masks and 46+κ-bit primes, with quantitative end-to-end error budget before implementation (and cost analysis of 4096 masks); or (B) PARK MOAI I126–132 if trivial mask/rescale work lacks significance and choose a fresh high-upside FHE target. No more generic scale folklore and no actual speedup claim.
STATE_UPDATE: YES — preserves explicit algebraically correct repair, quantifies cost and fatal matched-precision prime-size obstruction; I130 viability remains conditional.
