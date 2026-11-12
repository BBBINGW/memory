# BOOT / B158_OVERALL — Research Turn 24/25
## Galois-frame terminal product elision no-go

**Date:** 2026-11-12 (Asia/Singapore)  
**Phase:** PROBLEM_SELECTION  
**Candidate:** `boot-b158-galois-frame-terminal-product-elision-v1`  
**Decision:** FAIL_EXACT_SEMANTICS -> PARKED  
**Native/Codex:** NOT RUN

## Pre-registration

- **QUESTION:** Can the B175 terminal pointwise product `LT8(j) * y^(j mod 8)`, with `y=x^8192`, be replaced exactly by stock BGV Galois/rotation plus public-linear operations, eliminating the failing 26th ciphertext-ciphertext multiplication?
- **CURRENT_BELIEF:** Probably not. Galois/rotation is a plaintext-slot permutation and public lintrans is a fixed linear map; neither creates a bilinear interaction between the encrypted LT value and the encrypted grouped-power value. But a special B158 packed frame could in principle have encoded the phase twist into the slot orbit, so this must be checked exactly.
- **CHEAPEST_DECISIVE_TEST:** Work only at the exact plaintext-slot interface. Model every no-ct×ct candidate built from rotations/Galois, row swaps, public plaintext diagonals/scalars, additions/subtractions and public constants as an affine linear map of the encrypted operands. Exhibit one legal lower polynomial and four legal phases that force a contradiction.
- **IF_PASS:** Retain the candidate as the sole ACTIVE mechanism; next test stock key/interface feasibility and the all-in value ceiling.
- **IF_FAIL:** PARK the public-linear Galois-frame substitution family; do not infer impossibility for nonlinear fusion mechanisms that still use an encrypted multiplication elsewhere.
- **IF_UNCLEAR:** Keep no PASS and do not native-run.
- **WHICH_PAPER_GATE_CHANGES:** Killer gate (1), exact semantic/correctness oracle.
- **WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:** If valid, this mechanism deletes exactly the B175 multiplication that changes the residual budget from +16 to -15. If semantically impossible, source/noise/benchmark work is wasted.

## Closest source mechanism and exact delta

The closest stock primitive is BGV linear transformation / slot permutation.

Lattigo v6 at commit `aacd8b2c0c2c900d3063a30b8290e255463e1bb9` states:
- `schemes/bgv/evaluator.go`: `RotateColumns` calls a ring automorphism.
- `schemes/bgv/params.go`: the corresponding automorphism acts as a cyclic column rotation on batched plaintexts; the order-two row automorphism swaps plaintext rows.
- `circuits/bgv/lintrans/lintrans.go`: package comment says it implements **homomorphic linear transformations**; `Evaluate` is a sum of rotated vectors multiplied by public diagonal vectors.

Therefore any circuit composed solely of these primitives plus public scalar/plaintext multiplications and additions is an (mathbb F_T)-linear map on decoded SIMD values. Allowing public known constants makes the most general plaintext semantic form affine.

The candidate delta is to try to use this fixed public-linear machinery in place of the encrypted dynamic diagonal
[
D_y = operatorname{diag}(1,y,ldots,y^7)
]
that the current GROUPED ciphertext supplies.

## Durable B158/B174 semantics used

At the H=8192, s=8 B158 geometry:
- the lower polynomial has the Paterson-Stockmeyer decomposition
[
f_{<65536}(X)=sum_{i=0}^{7} X^{8192 i} f_i(X),qquad deg f_i<8192;
]
- ParallelLT produces the periodic block-value layout
[
L_f(x) = [f_0(x),f_1(x),ldots,f_7(x)]_{m periodic};
]
- B174 independently verified
[
G(x)_j = y^{jmod 8},qquad y=x^{8192}pmod{65537}.
]
The source target before the rotate-and-sum is
[
P_f(x)=L_f(x)odot G(x).
]

B165 source/audit fixes
[
T=65537,qquad x=(128m+e)mod 65537
]
for legal message/error pairs, with the tested legal domain including ordinary small errors such as (e=0,1).

## Exact affine-linear obstruction

Assume a terminal replacement contains **no ciphertext-ciphertext multiplication** and uses any number of:
- column rotations / row swap / Galois automorphisms,
- public plaintext diagonal/scalar multiplication,
- additions/subtractions,
- public known constants,
on the available ciphertexts (L_f(x)) and (G(x)).

At the decoded plaintext level, for a fixed public polynomial (f), its output has the form
[
O_f(x)=A_f L_f(x)+B_f G(x)+c_f
]
for fixed public linear operators (A_f,B_f) and public constant vector (c_f). The operators may depend on the public function (f), but not on the encrypted phase (x).

Choose the legitimate lower polynomial
[
f(X)=X^{8192+1}.
]
Then
[
f_1(X)=X,qquad f_i(X)=0;(i
eq1),
]
so the LT output contains the value (x) exactly in the residue-class-1 block positions and zero in the other block classes.

Focus on one output position (jequiv1pmod8). Since every coordinate of (L_f(x)) is either (0) or (x), and every coordinate of (G(x)) is one of (1,y,ldots,y^7), the most general affine-linear output coordinate is
[
O_j(x)=a x+q(y)
]
for a fixed public (ainmathbb F_{65537}) and some fixed public polynomial (q) of degree at most seven (the constant term absorbs (c_f)).

Exact correctness requires
[
a x+q(y)=xy
]
for every legal phase.

Because (8192) is even,
[
(-x)^{8192}=x^{8192}=y.
]
For any two legal phases (x) and (-x) with the same (y), subtracting the two correctness equations gives
[
2ax=2xy.
]
Since (T=65537) is odd and (x
eq0),
[
a=y.
]

Now use two exact legal sign-pairs from the B165 phase law.

### Pair 1
[
x=128=(128cdot1+0)mod65537
]
is legal with ((m,e)=(1,0)).

Its negative is
[
-128mod65537=65409=128cdot511+1,
]
legal with ((m,e)=(511,1)).

Exact modular exponentiation gives
[
128^{8192}equiv1pmod{65537}.
]
Hence the sign-pair argument forces
[
a=1.
]

### Pair 2
[
x=384=(128cdot3+0)mod65537
]
is legal with ((m,e)=(3,0)).

Its negative is
[
-384mod65537=65153=128cdot509+1,
]
legal with ((m,e)=(509,1)).

Exact modular exponentiation gives
[
384^{8192}equiv4096pmod{65537}.
]
Hence the same fixed operator forces
[
a=4096.
]

Contradiction:
[
1
eq4096pmod{65537}.
]

Therefore no public affine-linear circuit over the stock BGV slot operators can realize the required terminal product for the complete B158 lower-polynomial interface.

## What this no-go does and does not prove

It **does prove**:
- a pure Galois/rotation/public-lintrans replacement of the terminal pointwise multiplication is impossible for the generic B158 lower-polynomial evaluator;
- adding the existing GROUPED ciphertext only through linear operations does not help: the proof already allows an arbitrary linear term (B_f G(x));
- any exact replacement must introduce a genuine nonlinear interaction somewhere, or materially change the representation/contract so that the target is not the same bilinear map.

It **does not prove**:
- no special compiled shortcut exists for one single fixed LUT function;
- no nonlinear fused algorithm can move the encrypted multiplication earlier;
- no RGSW/external-product/keyed conversion can implement the dynamic diagonal more favorably;
- no restricted LUT family admits a special identity.

The monomial (X^{8193}) is used as an exact algebraic lower-polynomial counterexample. If a future paper claim is restricted to a smaller message-plateau LUT family that provably excludes this polynomial behavior, this specific no-go would need to be re-scoped rather than overextended.

## Gate disposition

1. **Exact semantic/correctness gate:** FAIL.
2. **Stock/source feasibility:** stock linear operations exist and their linear semantics are source-confirmed, but this cannot rescue the failed semantic gate.
3. **Optimistic value ceiling:** not reached. If the mechanism had passed it would have removed one ct-ct, but a semantically invalid construction has zero paper value.

No native experiment is justified.

## Decision

`boot-b158-galois-frame-terminal-product-elision-v1` is **PARKED**.

**NO_CREDIBLE_NEW_MECHANISM** remains for this candidate.

### Reopen condition

Reopen only with a materially different representation in which the desired (x^{8192j}) action is already encoded in the ciphertext coordinates or key material, or with a nonlinear source-compatible operation that implements the dynamic diagonal while recovering the B175 fixed-Q margin. The reopening evidence must include:
1. complete whole-output semantics on the actual LUT contract;
2. exact source type/key construction;
3. fixed-Q noise/DFR evidence;
4. all key/memory/offline/runtime costs;
5. independent novelty.

A larger set of rotations, different BSGS schedule, more public diagonals, or a different public permutation does not satisfy the reopen condition.

## Eliminated uncertainty

Whether the failing B175 terminal encrypted pointwise multiplication can be deleted merely by reinterpreting the (y^{jmod8}) grouped-power action as a stock BGV slot rotation/Galois/public-linear transform.

**Answer: no.** The target is a phase-dependent bilinear map; stock public-linear slot operators cannot implement it on the full B158 lower-polynomial interface. The exact legal sign-pair contradiction forces one fixed coefficient to equal both 1 and 4096.

## Evidence refs

- `findings/boot-B165-phase-robustness-artifact-audit-2026-10-28.md`, blob `459e7f9158053ca059d24c6c3ad70d6609aecdb3`: (T=65537), (Delta=128), phase law (x=(128m+e)mod65537), legal-phase native audit.
- `findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md`, blob `ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29`: exact GROUPED plaintext (G_j=y^{jmod8}).
- `findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md`, blob `49a85b46bf23566b24324e0994b7f2830b136dc5`: PS lower-polynomial decomposition / periodic block-value LT semantics.
- Lattigo v6 commit `aacd8b2c0c2c900d3063a30b8290e255463e1bb9`, `schemes/bgv/evaluator.go` blob `8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f`; `circuits/bgv/lintrans/lintrans.go` blob `1d4a33e9613ab27f931927ad8712afc67816b565`; `schemes/bgv/params.go` blob `af9d73c82c92fa4a58106d2d8d314ba0ea8785c3`.
- Turn-local exact arithmetic: (128^{8192}mod65537=1), (384^{8192}mod65537=4096), and the two legal sign-pair encodings above.
