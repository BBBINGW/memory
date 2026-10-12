# Iteration 125 — No free automorphism/external-product fusion with an ordinary online GGSW operand

Date: 2026-10-12 (Asia/Tokyo chronological session). PI authorized independent selection after I124; choose one concrete transfer hypothesis; ONE no-noise toy algebra falsifier. New paper branch; not a correctness allegation against cited authors.

## Source / provenance
Olivier Bernard and Marc Joye, *Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys*, ASIACRYPT 2025, IACR ePrint **2025/163**, https://eprint.iacr.org/2025/163, full original 37 physical pages acquired through Research MCP from verified GitHub ePrint mirror, SHA256 `ce81021fca19132729765ad652a2f4a8f1d27d6b9c7f084777b6386fa5e08387`, mirror revision `b4de82b1bf242bc0cf953c0a926d5cf88bfff12a`; official latest version `VERSION_UNVERIFIED`. Source anchors §4.1, physical pp14–15, Definition 4.1 (automorphism-extended gadget encryption), Definition 4.2 (fused product), Proposition 4.3 (noise), and §4.2 physical pp16–18 (additional ψ-specific bootstrapping-key copies and key size/cost trade-off, Algorithm 4.1). This is NOT a paper-wide technical audit or a claim of novel findings.

## Primary hypothesis and single decisive test
[HYPOTHESIS] The automorphism-parametrized external-product speedup from Bernard–Joye can be transferred unchanged to an online/dynamically produced *ordinary* GGSW operand, just by applying ψ to the first GLWE ciphertext and evaluating the existing ordinary external product, with **no automorphism-specific extended gadget ciphertext and no key switch**. This would extend the optimization beyond public precomputed bootstrap keys without extra evaluation-key formats.

[FALSIFIER/TEST] Compute ideal zero-noise decryption algebra for k=1 and exact gadget decomposition, using an ordinary GGSW for \barμ; if its plaintext under the original s contains a nonzero extra term when ψ(s)≠s, the claimed representation-only transfer is impossible.

## Source-grounded algebra and no-noise counterexample

Use author's GLWE sign convention: `(a,b)` is an encryption of μ under secret s when `b-a·s=μ` (zero error). Ordinary GGSW of \barμ under s supplies gadget rows encrypting `g·\barμ` and `-s·g·\barμ`. Definition 4.2's correct ψ-extended gadget instead contains rows encrypting `-ψ(s)·g·\barμ` while *ciphertexts themselves remain under s*.

[DERIVED] If one feeds the **ordinary** GGSW rows to the author's ψ-fused gadget arithmetic, in the exact-decomposition, zero-noise limit its output decryption under s is
```
  \barμ (ψ(b) - s ψ(a))
= \barμ ψ(μ) + \barμ ψ(a)(ψ(s)-s).
```
The target is only `\barμ ψ(μ)`. Thus the undesired extra is
```
  Err_semantic = \barμ ψ(a)(ψ(s)-s).
```
This is a **plaintext correctness error** even when encryption error = 0; cannot be treated as a noise-growth adjustment. It vanishes under special cases such as ψ(s)=s, ψ(a)=0 or \barμ=0, but is nonzero generically.

[DERIVED/ONE TOY TEST] Take `R=F_17[X]/(X^4+1)`, the legal cyclotomic automorphism ψ(X)=X³ (since gcd(3,8)=1). Choose `s=X, a=1, μ=1, \barμ=1`, with zero error and b=X+1. Then
```
ψ(s)=X³,       ψ(b)=1+X³,       ψ(a)=1,
ordinary-GGSW fused decryption:
    1+X³-X    !=    ψ(μ)\barμ = 1    in R.
extra=X³-X ≠ 0 mod (X⁴+1,17).
coefficient representation:
  actual = [1,16,0,1], desired = [1,0,0,0].
```
Independently verified via short local exact negacyclic multiplication and ψ substitution; no FHE implementation run. The demonstration applies to any exact gadget with correct reconstruction; for clarity a 1-digit gadget g=1 is sufficient (not claimed to be a secure parameter choice).

[NEGATIVE] The unrestricted **ordinary-online-GGSW** transfer hypothesis FAILS.

## Interpretation and decision
[FACT/PRIOR ART] This obstruction follows *directly* from Definition 4.1 of the original work, which already introduces ψ-specific encrypted rows precisely to account for ψ(s). It is therefore **NOT a new vulnerability, counterexample to the actual fused operator, or new publishable gap**. Author's intended use is precomputed bootstrapping keys; §4.2 explicitly trades their enlarged ψ-specific stored key set against fewer online automorphism key switches. Dynamically generated GGSW ciphertexts do not automatically arrive in that format. A public conversion to that format may require additional encrypted-key-dependent material or expensive homomorphic transformations, negating the proposed free transfer; this was not evaluated as a separate primary hypothesis.

[OPEN] Whether an alternate fused operator for online arbitrary GGSW without ψ-specific re-encryption can change the key-size/online-cost frontier is not established. A future viable project must propose a nontrivial mechanism and compare against traditional key-switch→external-product online cost and extra evaluation-key storage, including noise/security. No novelty proof or performance gain here.

## Iteration end
STATUS: **FAIL direct transfer / PASS exact algebraic falsifier / HUMAN_REVIEW**.
RESULT: `ordinary GGSW + ψ on first input` leaves `\barμ ψ(a)(ψ(s)-s)`, explicitly nonzero in a 4-dimensional cyclotomic toy ring. BJ25's `GLWE^{⊛,ψ}` eliminates exactly this term; their construction remains correct.
NEXT_ACTION: **PI decision** — PARK this ordinary-GGSW transfer as already resolved by original BJ25; authorize either (A) one separately sourced, genuinely new mechanism/setting for fused *dynamic* gadget products with a quantified key-size/noise frontier, or (B) select an entirely different FHE paper and hypothesis. Do not automatically turn the same source definition into more iterations.
STATE_UPDATE: YES — close I125 and preserve the no-noise negative result.
