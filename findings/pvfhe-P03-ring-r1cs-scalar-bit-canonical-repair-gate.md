# PVFHE-P03 — Canonical range is cheap; scalar-bit enforcement cannot be purely ring-polynomial for unanchored witness

**Checkpoint:** 2026-10-14 (Asia/Tokyo). **Independent PVFHE-P03 COMPLETED; P04 NOT STARTED.**
**STATUS:** **FAIL** proposed universal scalar-bit repair using only extra Ring-R1CS arithmetic constraints; **PASS** cheap source-specialized canonical range for genuine bits, PASS idempotent-gluing no-go, PASS correctness for an independently *already-anchored scalar public* input. **UNCLEAR** enriched primitive repair, compiled SNARG fraud, real attack advantage/novelty. NOT a claim of finished cryptographic attack.

## Read-before-write and source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` SHA `b365d3ef193734d0508e04753ed0558b7688752c` (concurrent vFHE), P01 `findings/pvfhe-P01-ring-r1cs-bitdecomp-xpow-source-parameter-counterexample.md` SHA `83ac7399bd0f12b9b6873a814d7b35e3625ebfdc`, and P02 `findings/pvfhe-P02-keyswitch-modswitch-full-evalgate-witness-gate.md` SHA `9b09262066c61778ce581abbba4dbd5098ee5483`. P02 proved *source-level* composed EvalGate ciphertext mismatch 0 vs1023 using x0=x2=x53=1 encoding Q for extracted a0=0, without a real SNARG transcript. Target P03 absent before writing. **Do not edit** any existing state, independent SHIP/vFHE, P01 or P02.

**Original paper [FACT]:** Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint `2024/1764` https://eprint.iacr.org/2024/1764. Original full PDF acquired from Research MCP Github mirror, **29 pages**, PDF SHA256 `7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089`, **VERSION_UNVERIFIED**. Inspected physical p15 Lemma4.5, Claim4.6 bitness/bit-decomposition over `R_Q`; p16 Lemma4.8/4.10/4.11; p17 Lemma4.11 proof and Theorem4.12; p26 AppendixB original `Q=2^53+5,N=2048` and Appendix C.1. Source math-extraction warnings; official revision parity unverified. The source explicitly restricts the R1CS language to ring arithmetic equations (`+`, `*`, `=`) with auxiliary witnesses, and assumes `x²=x⇒x=0 or1` in that ring (P01 refuted literal claim).

## ONE primary hypothesis + ONE decisive test

**[HYPOTHESIS P03]** A special-Q canonical integer range comparator using `O(log Q)` only-ring constraints, appended to existing `BitDecomp`, **also** forces witness bits to be public **SCALAR** values 0 or1 for arbitrary *unanchored intermediate* ring variables, repairing P01/P02 without extra proof primitives or cross-component checks.

**[FALSIFIER]** Derive exact canonical comparator for scalar bits; construct a nontrivial idempotent witness that passes comparator but is NOT scalar, and prove the stronger closure theorem that ANY existential polynomial equations over a ring with a central nontrivial idempotent can splice valid zero and one witnesses to admit a non-scalar bit for the same fixed public parameters. Check the different case of an independently *already-anchored* scalar public input to avoid an overbroad negative result. One test batch on toy split ring and source actual Q,N with exact arithmetic.

## Conditional easy comparator [DERIVATION / PASS]

At `Q=2^53+5, ell=53`, write `S=Σ_(j=0)^53 2^j x_j`, `h=x_53`, `H=Σ_(j=3)^52 2^j x_j`. **IF** each `x_j` is genuinely a scalar Boolean bit, `0≤S<Q` is equivalent to the following two ring equations:
```
   h * H = 0,
   h * x_2 * (x_0+x_1-x_0*x_1) = 0.
```
If h0, S<2^53<Q. If h1, high condition H=0 modulo Q implies **integer H=0** because 0<=H<2^53<Q, and second condition forces x2=0 or (x0=x1=0), giving low part 0..4. Hence S≤2^53+4, canonical. Conversely every canonical 54-bit S passes. Reusing S and low bits allows H construction with constant many extra weighted ring additions and ~4 extra multiplies, not worse than `O(log Q)` gadget. This kills P01/P02's `S=Q` scalar-bit witness, **conditional on scalarity**.

## The nontrivial idempotent and universal gluing obstruction [DERIVATION / FAIL proposed complete repair]

The actual source ring is `R_Q=F_Q[X]/(X^2048+1)` with prime `Q=9007199254740997`, verified exact. Let `i=5673791807417170 modQ`, `i²=-1`. The nonconstant element
```
 e=(1+i X^1024)/2
  =4503599627370499+2836895903708585 X^1024 (modQ,X^2048+1)
```
obeys `e²=e`, `e(1-e)=0`, `e≠0,1`. Assign `x_0=e`, all remaining bit variables0, and reconstructed free `S=e`: x_i²=x_i and **BOTH** comparator equations hold (h=0); but the only nonzero bit is NOT a scalar bit and y=S is not a constant polynomial.

**Generalized ring-only impossibility:** For ANY commutative ring R with a nontrivial central idempotent e, and ANY system of existential polynomial equations `f_j(x,u;public_constants)=0` over R which admits a valid witness with x0 and one with x1 for the SAME fixed public constants, the combined assignment `(x,u)=e(1,u_1)+(1-e)(0,u_0)` is also valid. For each polynomial f, `f(eW_1+(1-e)W_0)=e f(W_1)+(1-e) f(W_0)=0`. The public constants are fixed because `ec+(1-e)c=c`. Thus **no number of only-ring arithmetic constraints with arbitrary existential auxiliaries can express the standalone predicate `x∈{0,1}⊂R` for a FREE/unanchored ring element**, while accepting both bits. This is an elementary direct-product ring fact, NOT an unconditional lower bound for richer non-ring primitives or FHE verification systems.

**Important anchored-input distinction:** Q is prime and X^2048+1 squarefree modulo Q (N invertible), so R_Q decomposes into a finite product of fields. Idempotence projects to ordinary 0/1 in each factor. If reconstructed y is independently forced to a KNOWN SCALAR `a∈F_Q` in *every* factor, the comparator constrains each factor's bit-sum to a unique integer `S∈[0,Q-1]`; all factor values coincide with a, so binary uniqueness enforces identical 0/1 bits across factors. Therefore `canonical bound + idempotence + trusted scalar public y` **CAN** repair this narrower anchored case. The no-go concerns **free intermediate values**, which matters for the source Lemma4.11's attempt to infer scalar coefficients from BitDecomp itself. The original source does not independently supply a trusted scalar anchor for every such extracted witness; assuming it would be circular.

## ONE executed exact minimum verification

- Script `/mnt/data/pvfhe_p03_scalar_canonical_gate.py`, SHA256 `ff29fd46008e6e1d203ae104e3f263b6c14d58442e322668814bfc3d109fb9a9`.
- JSON `/mnt/data/pvfhe_p03_scalar_canonical_results.json`, SHA256 `b06b70d66733240098fce1db3cfd42a51126945c784afb4f597b9fc205fa8b5d`.
- Full local report `/mnt/data/PVFHE_P03_Scalar_Bit_Canonical_Ring_R1CS_Gate.md`, SHA256 `c73e5650aa6c2e10235815a45f94bec96ddefff1f4683495bc3e4c9c81836159`.
- Actually executed: real Q primality, i²=-1, e²=e, comparator rejects P02 bit integer Q but accepts canonical 0..Q−1 test values.
- Exact exhaustive small valid analogue `R=F37[X]/(X^4+1)`, `Q=2^5+5`, nontrivial idempotent e=19+3X²: all 4^6=**4096** tuples of idempotent-valued six bits enumerated. Canonical comparator accepts 37²=**1369** tuples: 37 reconstruct scalar y (with **all** bits scalar and uniquely canonical); **1332** reconstruct NONscalar y. The explicit x0=e and all others0 passes. This directly illustrates one equation's success for an independently scalar y and simultaneous failure for free y.
- No compiled FHE proof, complete SNARG matrices/transcript, new cryptographic complexity lower bound, or realistic false-plaintext attack executed.

## Research decision / end of iteration

**STATUS:** FAIL all-ring unrestricted scalar-bit repair under claimed model; PASS cheap conditional canonical bound and universal free-variable idempotent-gluing theorem; UNCLEAR efficient enriched proof primitive or full system attack/novelty.
**RESULT:** Source bit-sum ambiguity S vs S+Q can be cheaply fixed **when scalarity is trusted**. But the more fundamental Claim4.6/Lemma4.11 scalarity boundary cannot be repaired by ANY amount of the same ring-polynomial constraints for genuinely unconstrained coefficient witnesses. Must introduce a **cross-component primitive**, independently anchor inputs to a scalar, or change proof representation. This is an algebraic technique obstruction, not automatically publishable new crypto.
**NEXT_ACTION PVFHE-P04 only on PI continuation:** ONE source-costed cross-component primitive gate, e.g. scalarity enforced via automorphism invariance or coefficient trace and demonstrated outside the ring-only closure model. Check actual operation/proof costs and security vs previous work; distinguish Galois linear maps from allowed ring multiplication. Else escalate HUMAN_REVIEW, do not recycle comparators/toy rings.
**STATE_UPDATE:** YES standalone P03 findings only. No edits to concurrent vFHE STATE.md, SHIP state, prior P01/P02 or other archives.
