# Iteration 131 — The CKKS scale-one half-wise 0/1 boundary mask is not precision-free

Date: 2026-10-13. PI authorized I131 after I130. ONE primary falsifiable hypothesis and ONE cheap canonical CKKS encoding/level-alignment test. NO compiled SEAL/OpenFHE, NO encrypted/noisy CKKS runtime, NO practical latency measurements; do not mislabel a plaintext encoder simulation as an actual CKKS encryption run.

## Read-before-write / sources

- Latest `STATE.md` I130 SHA `d5b8d13be2171c0c01c385f81e1cdd3f1d322536` read before edit; I130 result `findings/moai-native-paired-bsgs-halfwise-rotation-cost-iteration130.md`, SHA `3f9c122def303f70aa12e99754b2136a2499fed8`, read in full.
- Original MOAI: Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ICLR2026 / IACR ePrint **2025/991**, https://eprint.iacr.org/2025/991, previously full 32-physical-page GitHub ePrint mirror PDF SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, official VERSION_UNVERIFIED; Appendix B Algorithm4 p20 BSGS with rotations of ciphertexts; §6 p10–11 standard approximate CKKS scale/multiplicative depth.
- Original Microsoft SEAL official CKKS encoder and scale documentation, inspected current GitHub source:
  https://github.com/microsoft/SEAL/blob/main/native/examples/2_encoders.cpp (scaled CKKS vector encoded into integer-coefficient polynomial; scale sets precision)
  https://github.com/microsoft/SEAL/blob/main/native/examples/5_ckks_basics.cpp (`multiply_plain` and Ct×Ct scale multiplication and `rescale_to_next` consumes one modulus prime)
  https://github.com/microsoft/SEAL/blob/main/native/src/seal/ckks.h (encoder accepts an explicit `scale`).
- NO CKKS library was installed in this runtime; experiment below is an *encoder-equivalent idealized canonical-embedding and integer-coefficient nearest-rounding simulation*, NOT a real SEAL execution and not representative of high-security MOAI parameters.

## ONE hypothesis and cheapest decisive falsifier

[HYPOTHESIS] The half-wise rotation boundary mask `J_k` required in I130 can be encoded as a CKKS plaintext at **scale Δ_M=1**, used after Ct×Ct multiplication with high precision, thereby avoiding any scale change or extra rescale and retaining I130's reported KS/count frontier unchanged.

[FALSIFIER / ONE TEST] Encode the explicit nonconstant J mask via canonical inverse embeddings and coefficient rounding at several plaintext scales, then decode it and apply it to the exact two-global-rotations halfwise operation. At Δ_M=1, if the mask has substantial off/on slot errors and produces a wrong halfwise output even before RLWE noise, the scale-one precision-free claim is false. Cross-check the standard CKKS scale bookkeeping for Δ_M>1 using SEAL's official examples.

## Algebraic key observation

I130 defines `S=2H`, a ciphertext with two *different* length-H halves, and for any `0<k<H`:
```
 T_k(C)=Rot_k(C)+J_k⊙[Rot_{k−H}(C)−Rot_k(C)]
 J_k[j]=1  iff  (j mod H) >= H−k; otherwise 0.
```
As an exact complex SIMD vector, J is a nontrivial 0/1 selector. But in standard CKKS plaintext `p(X)∈Z[X]/(X^N+1)`, a **nonzero p(X) of degree <N cannot vanish at a primitive 2N-th root**: minimal polynomial `Φ_{2N}(X)=X^N+1` is irreducible, so if any complex embedding `p(ζ^{odd})=0`, then p=0. Therefore a nonconstant 0/1 slot mask is NOT an exact integer-poly CKKS plaintext at ANY finite scale — it needs approximate encoding. (This is about the integer polynomial canonical embedding, NOT CRT mod-q idempotents with potentially large coefficients/security cost.)

## One reproducible idealized encoder test

Take `N=16`, `R=Z[X]/(X^16+1)`, `S=N/2=8` slots, `H=4`, `k=2`; target
```
 J = [0,0,1,1 | 0,0,1,1].
```
Use slot embeddings `ζ^(5^j mod 2N)`, `ζ=exp(πi/N)`, for j=0..7; fill conjugate embeddings with matching real values. Interpolate to unique real degree-<16 polynomial `p∈R[X]` with desired embedding values; for chosen scale `Δ_M`, round each coefficient of `Δ_M p` to the nearest integer, then decode and divide by `Δ_M`. Integer rounding is the ideal canonical-embedding model used for this falsifier; specific SEAL FFT and tie-breaking order may differ in low precision.

```
scale Δ_M      max absolute decoded slot mask error
1              1.000000 (constant 0 or 1 depending midpoint tie)
2^4            0.02985297164
2^8            0.00375931216
2^12           0.00007040672
2^16           0.00000717644
```

Using `C=[2,-3,5,7 | 11,-13,17,19]`:
- correct halfwise T_2 output: `[5,7,2,-3 | 17,19,11,-13]`.
- if `J` decodes to all ones with scale-one nearest-rounding, computed output is `[17,19,2,-3 | 5,7,11,-13]` (max absolute wrong-entry error 12); all-zeros variant likewise wrong.
- at scale 2^4 the maximum halfwise output error in this toy is ≈0.35823566; 2^8 ≈0.04511175; 2^12 ≈0.000844881; 2^16 ≈0.0000861173.
Thus the **exact binary mask free at scale 1** fails in plaintext encoding before any CKKS encryption/rounding/noise. This is **not** a counterexample to I130's exact-slot BSGS formula.

Additional equivalent toy results at N32 and N64, mask choices 1,2,4,8, likewise show max slot error 1.0 at scale1 and convergence as scale rises, so it is not a peculiarity of a single N16 vector.

## CKKS scale / level bookkeeping and hard scope

Let current ciphertext scale be Δ and plaintext mask scale Δ_M. For CKKS `multiply_plain` gives scale ΔΔ_M. For the halfwise identity `A + (B−A)⊙J`, branch A has scale Δ and the masked branch has scale ΔΔ_M; adding requires scale alignment and matching encryption modulus.

If Δ_M=1, scale algebra is aligned but numerical mask fails at least in the canonical rounding model tested. If Δ_M large (as usual for accurate nonconstant masks), naïve execution:
1. after regular Ct×Ct multiply at scale ≈Δ², rescale once ≈Δ (original baseline);
2. implement `T_k` mask at scale Δ_M≈Δ, yielding ≈Δ² in masked branch;
3. rescale masked branch back to ≈Δ, modswitch unmasked branch, then add.

**In this straightforward schedule the post-Ct×Ct giant halfwise mask costs an additional rescale level** (relative to BSGS without that mask) and rounding. Pre-hoisted halfwise rotations/masked baby terms may incur levels on their respective operand paths too. At m128,t8,g8 I130 counts 1016 Ct×Pt masks (56 hoisted pre-halfrot, 512 baby masks, 448 post-Ct×Ct giant masks). Post-product masks on the critical path are specifically a significant potential level obstruction.

However, **not an impossibility theorem:** one may defer rescale, use smaller Δ_M with a quantified error budget, multiply the unmasked branch by an integer scale-alignment factor, or algebraically move halfwise masks to before the Ct×Ct multiplication. These may trade bits of modulus or more masks/rotations for fewer rescale levels. No exact-parameter SEAL or Phantom experiment was run. Therefore only the **scale-one free-precision shortcut is FAIL**; the whole I130 native paired BSGS scheme remains **UNCLEAR** pending a new mechanism/source-specific CKKS test.

## Novelty and interpretation

CKKS scaling and approximate mask encoding are standard issues, not a new cryptographic error or publishable novelty. I130's schematic KS reduction of 9652→6128 remains a **count under ideal mask and key-switch assumptions**, not a verified CKKS performance advantage. Any next meaningful iteration should test a concrete scale-compatible halfwise implementation under exact parameters/levels, not repeat scalar masking folklore. Native paired half-batch B≤128 also cannot be called better throughput than published MOAI B256.

## End of iteration
STATUS: **FAIL scale-1 precision-free mask / PASS ideal canonical-encoder falsifier / UNCLEAR full I130 CKKS feasibility / HUMAN_REVIEW**.
RESULT: J_k is necessarily approximate in CKKS; an explicit N=16 scale-1 encoding loses its nonconstant selector (1.0 max slot error) and a halfwise rotation gives incorrect plaintext output. At Δ_M≫1 ordinary multiply_plain changes scale and straight-line rescaling creates a potential extra level on the post-Ct×Ct critical path. Does not invalidate I130's noiseless algebra or prove all scale propagation tricks fail.
NEXT_ACTION: PI gate for I132. Recommend ONE smallest specific hypothesis: can the **post-multiplication giant halfwise mask be moved to pre-multiplication operands / combined with a scheduled rescale** without adding depth or erasing the I130 KS advantage? Cheapest algebraic gate should quantify additional masked operands and operations at m=8 first. Alternatively PI PARKs the entire MOAI I126–131 optimization if effort/novelty not justified. Do not assert a compiled CKKS test where none exists.
STATE_UPDATE: YES, important feasibility blocker and negative result for direct free-mask assumption.
