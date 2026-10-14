# PVFHE-P01 — Exact source-parameter counterexample to Ring-R1CS BitDecomp and XPow

**Date:** 2026-10-14 (Asia/Tokyo). **Independent FHE+proof systems stream:** PVFHE-P01 COMPLETED, P02 NOT STARTED. **STATUS:** PASS exact modular-ring witness; FAIL local lemma implication “satisfying XPow constraints imply y=X^alpha” for concrete source parameters; FAIL literal universal idempotent claim; HUMAN_REVIEW complete EvalGate/Ring-R1CS and SNARG soundness. This is NOT evidence of a complete public proof forgery or FHE cryptographic break.

## Read before write / source / isolation

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (parallel vFHE), `findings/nested-rns-N02-rescale-error-integer-bound-gate.md` SHA `d9b64b40bccce42b6726b89794307ceede8f980c`, research backlog, latest separate SHIP state; inspected findings/ and failures/ names, no existing subject `2024/1764` / pvFHE / ring-R1CS issue archive. This new branch follows PARK of NRNS-N02 and SHIP radix microaudit. **No writes to shared STATE, SHIP, backlog or independent vFHE docs**.

Primary original: Mi-Ying (Miryam) Huang, Baiyu Li, Xinyu Mao, Jiapeng Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint **2024/1764**, https://eprint.iacr.org/2024/1764 (2024-10-29 preprint). Research MCP READY 29pp full mirror PDF SHA256 `7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089`, VERSION_UNVERIFIED; accessible IACR PDF web text cross-checked, screenshot **cache miss**; no authenticated binary/publisher-version parity certification. Physical p15 Lemma4.5 and Claim4.6, p16 Lemma4.10, p17 Theorem4.12, p26 Appendix B concrete params and Appendix C.1/C.2, p27 C.3 global argument.

## ONE primary hypothesis / ONE decisive test

**[HYPOTHESIS P01]** Under source concrete ring `R_Q=Z_Q[X]/(X^N+1)`, the Ring-R1CS `XPow(y;alpha)` constraint system of Lemma4.10, relying on the paper's `BitDecomp` of Lemma4.5, uniquely enforces `y=X^alpha` for public scalar `alpha=0 ∈Z_q`, even against arbitrary **satisfying-witness** bit assignments.

**[FALSIFIER]** Exhibit source-legal Boolean scalar bit values `x_i∈{0,1}` satisfying all `x_i²=x_i` and modular reconstruction `alpha=Σ 2^i x_i (mod Q)` yet causing the binary fast-exponentiation recurrence to give `y≠X^alpha` in `R_Q`. One such witness suffices to reject the LOCAL semantic lemma, not the whole published security theorem. Independently inspect the Claim4.6 idempotent premise on same parameters as an extra consequence, not a separate main hypothesis.

## Source facts

- Paper §4.2 Lemma4.5, physical p15: `ell=floor(log2 Q)`, **bits are x_0,...,x_ell INCLUSIVE**, ring constraints `x_i²=x_i` plus `y=Σ_i2^i x_i`; does not include `0<=Σ_i2^i x_i<Q` INTEGER range or scalar-constant bit-membership constraints separate from purported Claim4.6.
- Lemma4.10 p16: `XPow(y;alpha)` uses Lemma4.5 bits and branch products `X^(2^i)`; it claims every satisfying assignment has alpha scalar, output `X^alpha`.
- Appendix B p26: **Q=2^53+5=9007199254740997**, **N=2^11=2048**, **q=1024**, Q≡5 mod8 (chosen for PCS). Therefore ell=53, `X^2048=-1`, `X^4096=1`, `Q mod4096=5`.
- Claim4.6 p15 and LemmaC.1 p26 assert every `z²=z` in R_Q is literally 0 or1, using a Galois-ring lemma and assertion `R_Q/(p)≅F_{p^N}`. This ring is reducible at source parameters and has explicit nontrivial idempotents.

## Exact primary counterexample [DERIVATION & VERIFIED]

Fix **public input alpha=0**, embedded Z_q→R_Q. Its standard binary assignment `x_i=0` gives alpha0 and XPow result `X^0=1`.

Instead use the following **ordinary scalar bits only**:
```
 x_0=x_2=x_53=1,  x_i=0 otherwise,  for i=0,...,53.
```
All bit Booleanity constraints are satisfied, because each is 0/1. Modular reconstruction also holds in the *source ring*:
```
  Σ_i2^i x_i = 1+4+2^53 = Q = 0 mod Q = alpha.
```
But the XPow multiplication recurrence evaluates the exponent over integers, not modulo Q:
```
  y = X^(1+4+2^53) = X^Q = X^5 != 1 = X^alpha,
```
since `Q≡5 mod4096` and `X^4096=1`. The distinct canonical ring polynomials 1 and X^5 establish a **satisfying witness of the displayed source local Ring-R1CS relations that computes the wrong power for the same public alpha**. This is independent of cryptographic noise and requires NO nontrivial idempotent.

**Source-correctness implication:** BitDecomp modular equality does not enforce the UNIQUE canonical integer representative in [0,Q−1]. Including bit x_ell allows the ordinary 54-bit integer Q itself, so even all bits literal 0/1 gives multiple representations for alpha0. A future repair requires enforcing canonical range or equivalent exponent-aware consistency; relying only on modular bit sums is unsound.

## Secondary independent Claim4.6 algebraic obstruction [DERIVATION & VERIFIED]

Choose `i=2^((Q-1)/4) modQ=5673791807417170`; exact multiplication gives `i²≡−1 modQ`. Let `u=i X^1024`, so `u²=i² X^2048=(-1)(-1)=1`. Then
```
 e=(1+u)/2
  =4503599627370499 + 2836895903708585 X^1024 mod(Q,X^2048+1).
```
Since `u²=1`, `e²=e`; `e≠0,1` because its X^1024 coefficient is nonzero. This falsifies the literal ring claim `z²=z ⇒ z in {0,1}` for the very same AppendixB modulus and degree, and makes the Appendix C.1 finite-field/Galois-ring premise inapplicable without more hypotheses. This independent issue cannot be repaired merely by restricting the integer BIT SUM below Q: one must also ensure scalar Booleanity (possibly via a suitable dedicated embedding/constraint).
These two failures are **separate algebraic facts**, with the XPow alpha0/Q witness alone decisively falsifying the one primary hypothesis.

## Executed code and source quality

Actually executed Python source `/mnt/data/pvfhe_p01_xpow_noncanonical_bit_witness.py`, SHA256 `09befae3fe7c7aade29fdba52f0894302c64ef27bee3d6e1b91b630672685ee3`. JSON `/mnt/data/pvfhe_p01_xpow_noncanonical_bit_results.json`, SHA256 `4d3795d8feaa5926a8df91aab4490d7e6e8980f2214954f8cc123e4838eabc5f`. Full readable local research note `/mnt/data/PVFHE_P01_Ring_R1CS_BitDecomp_XPow_Counterexample.md`, SHA256 `fcfcc794e6f76213f53269fca9e91413b9ca31e5094f66d8478fd4b4ff43f304`. Pure exact integer ring arithmetic and explicit satisfying bit witnesses; no compiled FHE or SNARG, PCS-opening, fiat-shamir forged transcript, or target security experiment. Search did not expose a dedicated published erratum, **NOT** evidence no corrections exist.

## Scientific scope / recommendations

**[FACT]** Source Lemma4.5, Claim4.6, Lemma4.10 and AppendixC.1 use incorrect unchecked properties of R_Q / modular bit reconstruction under the stated concrete Q,N.
**[DERIVED]** Local relation admits wrong exponentiated polynomial, so the global Theorem4.12 iff proof relying on those lemmas has an **unfilled local soundness obligation**. Whether other FHE.Eval constraints eliminate every such witness remains unverified. Proof-system soundness for the *encoded wrong relation* is distinct from correct relation-to-FHE compilation.
**[OPEN]** End-to-end false-output Ring-R1CS witness; author/publisher version parity; cheap repair enforcing bit scalarity and canonical range without losing ring-native performance; any existing erratum or exploitation.
**[RECOMMEND]** CONTINUE / HIGH-PRIORITY HUMAN_REVIEW relative to archived SHIP radix and NRNS no-wrap because this is an exact source-parameter local lemma counterexample directly linking FHE and proof systems. **No contacting authors or public allegations without PI permission.**

**STATUS:** FAIL the local Lemma4.10 claimed implication and the literal Claim4.6; PASS exact algebraic source-param witness; UNCLEAR global FHE correctness/IND-SA/SNARG impact.
**RESULT:** `alpha=0` permits scalar Boolean bits encoding Q and forces XPow output `X^5 ≠1`; a separate nonconstant idempotent disproves the claimed bitness predicate.
**NEXT_ACTION — PVFHE-P02 only on PI continuation:** ONE minimal **full EvalGate relation lifting test**: trace source's ACC.Update α=0 branch and whether fake XPow X^5 can be assigned consistently across subsequent constraints to yield a wrong FINAL public output ciphertext, or whether other canonicality checks kill it. If no full witness, keep only local lemma refutation; do not claim SNARG forgery. Then assess a minimal repair with explicit scalar bits and strict <Q canonical range, cost/prior art, and verify authenticated paper edition.
**STATE_UPDATE:** YES this standalone PVFHE-P01 file only; NO edits to shared state, parallel vFHE/SHIP, NRNS prior notes, or backlog.
