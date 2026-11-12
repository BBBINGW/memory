# BOOT / B158_OVERALL — Turn 23/25
## SI subgroup Hermite noise-cleaning preflight

**Date:** 2026-11-12  
**Phase:** PROBLEM_SELECTION  
**Candidate:** `boot-b158-si-subgroup-hermite-noise-clean-v1`  
**Decision:** FAIL_NOVELTY_COLLISION / FAIL_OPTIMISTIC_VALUE_CEILING -> PARKED

## Pre-registration

- **QUESTION:** Can the fixed-Q B158/B175 terminal SI failure be rescued by applying a first-order identity/noise-cleaning polynomial to the order-2 selector carrier before the final multiplication, without changing the LUT semantics?
- **CURRENT_BELIEF:** The algebra can cancel first-order selector error, but the obvious cubic cleaner is likely prior art and costs two additional SI multiplications.
- **CHEAPEST_DECISIVE_TEST:** (i) exact local semantic/Jacobian oracle for the cleaner; (ii) bounded closest-prior-art check; (iii) optimistic static value ceiling using the already-measured B175 SI growth.
- **IF_PASS:** initialize as sole ACTIVE candidate and proceed to source-typed canary.
- **IF_FAIL:** PARK; do not native-benchmark or rename the idea.
- **IF_UNCLEAR:** keep no scientific PASS; do not native-run until novelty/value are resolved.
- **WHICH_PAPER_GATE_CHANGES:** PROBLEM_SELECTION / NOVELTY_PREFLIGHT, with an optimistic VALUE ceiling.
- **WHY DECISION-CHANGING:** a prior-art collision or zero-margin intermediate makes a source/native canary wasteful; surviving both would justify it.

## Rejected construction

Let the B175 carrier be the order-two plaintext selector `u in {+1,-1}` carried by `Y4`. Write a normalized BFV/SI decryption value as

[
z = Delta u + e,qquad Delta approx Q/T.
]

The minimum-degree identity Hermite cleaner at (pm1) is

[
C(x)=rac{3x-x^3}{2}.
]

It satisfies

[
C(1)=1,; C(-1)=-1,; C'(1)=C'(-1)=0.
]

Equivalently, for (x=u+arepsilon) with (u^2=1),

[
C(u+arepsilon)
= u-rac{3u}{2}arepsilon^2-rac12arepsilon^3.
]

Thus in the ideal scale-invariant arithmetic model the first-order selector error cancels:

[
Delta C(u+e/Delta)
= Delta u-rac{3u e^2}{2Delta}-rac{e^3}{2Delta^2},
]

before adding fresh tensor/quantization/relinearization errors from evaluating the polynomial.

A stock implementation needs two additional ciphertext-ciphertext multiplications:
1. (z_2=operatorname{SI}(z,z));
2. (z_3=operatorname{SI}(z_2,z));
3. (z_{m clean}=(3z-z_3)/2) using plaintext/scalar operations.

This is locally value-preserving on the (pm1) carrier. It is **not** a complete B158 correctness proof: source scale/carry/rounding and whole-output semantics were deliberately not expanded after the decisive novelty/value failure.

## Source feasibility evidence used only for the static screen

Lattigo v6 source at commit `aacd8b2c0c2c900d3063a30b8290e255463e1bb9`:
- `schemes/bgv/evaluator.go`: `tensorScaleInvariant` performs Q->QMul centered mod-up, low-degree tensor, `quantize`, then optional `GadgetProduct` relinearization.
- `schemes/bgv/evaluator.go`: `quantize` performs `ModDownQPtoP` (QP/Q -> P), `ModUpPtoQ`, multiplication by plaintext modulus (T), then NTT.
- `ring/basis_extension.go`: `ModUpQtoP` explicitly centers around (Q/2) before exact basis conversion.

Therefore the cubic can be expressed with existing SI/scalar interfaces; there is no free one-multiplication cubic identity available from these interfaces.

## Optimistic value ceiling

Durable B175 measurements give the order-two carrier `Y4` required-bits about 586 and roughly +31 required bits for each comparable SI carrier multiplication. The optimistic cubic chain therefore lands around:

- `Y4`: 586
- `Y4^2`: ~617
- `Y4^3`: ~648

against the fixed positive-budget ceiling around 648 bits. Hence the cubic intermediate has essentially no robust DFR margin even before a matched canary. It also raises the B175 ciphertext-ciphertext multiplication count from 26 to 28. The candidate can have an attractive **post-cleaning** symbolic error only if the cubic intermediate itself remains valid; that is not a robust optimistic end-to-end value proposition.

This is a ceiling screen, not a measured performance claim.

## Closest prior art and decisive collision

IACR ePrint 2024/1623, *General Functional Bootstrapping using CKKS*, explicitly describes polynomial Hermite interpolation as a noise-cleaning mechanism. It states that prior works use Hermite interpolation with (p=2), (f(x)=x), at (-1,1) or (0,1), and that CKKL24 uses order-one Hermite interpolation at power-of-two roots of unity. This subsumes the technical core of the proposed (pm1) identity cleaner: preserve the special plaintext points while forcing first derivative zero.

Therefore transferring the same derivative-zero identity cleaner to this BGV SI carrier, without a new source-specific theorem/interface that changes the cost frontier, is not a credible new paper mechanism.

Primary public evidence:
- ePrint 2024/1623, noise-cleaning/Hermite discussion (searchable passage around Eq. (23), Section 3.x / physical p19 in the indexed PDF).
- Lattigo v6 commit `aacd8b2c0c2c900d3063a30b8290e255463e1bb9`, files above.

## Decision

**PARKED.**  
Reason is conjunctive:
1. **NOVELTY COLLISION:** derivative-zero Hermite cleaning at (pm1)/roots of unity is explicit prior art.
2. **OPTIMISTIC VALUE CEILING FAIL:** the minimal cubic requires two extra SI multiplications; the second intermediate projects to the fixed-Q boundary and the count rises 26 -> 28.

No native task is justified. This candidate must not be renamed into a new ACTIVE line.

### Reopen condition

Reopen only with concrete evidence of a distinct source-specific mechanism that is not ordinary Hermite/root-of-unity identity cleaning, plus a complete typed schedule showing a robust sub-648-bit intermediate/final DFR margin, matched security/evaluation-key costs, all-in value over the original comparator, and an independent novelty audit.

## Eliminated uncertainty

Whether the obvious first-order-cancelling (pm1) identity/Hermite cleaner is a new low-cost B158 rescue. It is not: the mathematical mechanism collides with explicit prior art and its minimum cubic realization has no robust fixed-Q value margin in the current B175 geometry.
