# BOOT / B158_OVERALL — Research Turn 25/25
## Terminal co-packed accumulator/power fusion value gate

**Date:** 2026-11-12 (Asia/Singapore)  
**Phase:** PROBLEM_SELECTION  
**Candidate:** `boot-b158-terminal-copacked-accumulator-power-fusion-v1`  
**Decision:** PASS_EXACT_SEMANTICS / PASS_STOCK_SOURCE / FAIL_CALIBRATED_FIXED_Q_VALUE_CEILING -> PARKED  
**Native/Codex:** NOT RUN

## Pre-registration

- **QUESTION:** Can the B158 terminal lower-polynomial path co-pack the current LT accumulator and the current power (y^{2^i}) in the two BGV rows, so that one SI ciphertext multiplication per bit simultaneously updates the accumulator and squares the power, thereby replacing B174 GROUPED generation + B175 pointwise + the projected leading square?
- **CURRENT_BELIEF:** The recurrence should be algebraically exact and source-realizable using the same row-swap/mask/SI primitives as B158, with a meaningful ct-ct count reduction. The main risk is fixed-Q noise: the LT accumulator would now lie on a three-deep SI dependency chain, whereas the failed B175 design applies only one terminal SI multiply to LT.
- **CHEAPEST_DECISIVE_TEST:** (1) exact slot-level recurrence proof and toy exhaustive/random checks; (2) stock Lattigo interface audit for row swap, public mask, scale-one ct-pt and SI ct-ct; (3) optimistic fixed-Q value/noise ceiling calibrated only from B174/B175 measured same-parameter SI increments, granting zero public-mask cost.
- **IF_PASS:** If the three-deep fused terminal path has a credible positive fixed-Q margin under a source-backed model, retain as the sole ACTIVE candidate and make the next decisive test one small same-parameter native correctness/noise canary.
- **IF_FAIL:** If even the optimistic calibrated model lands at/above the B175 failure region, PARK; do not use the 3-ctct count win to justify native work without a new noise-contraction mechanism.
- **IF_UNCLEAR:** If a source-backed covariance/carry mechanism could plausibly lower the fused SI increments below the calibrated minimum, keep that as a distinct future mechanism requiring concrete evidence; do not infer it from packing alone.
- **WHICH_PAPER_GATE_CHANGES:** exact semantic/correctness oracle, stock/source feasibility, and optimistic end-to-end value/noise ceiling.
- **WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:** This construction is the first screened terminal mechanism here that both removes the failing B175 pointwise multiplication and simultaneously computes the leading power with fewer ct-ct operations. If its fixed-Q value ceiling still fails, the remaining issue is not operation count but a genuinely new noise/carry law.

## Exact construction

Fixed B158/B174 geometry:
- (N=32768), two batching rows of length (N/2=16384);
- (T=65537);
- (H=8192), (s=8);
- (y=x^{8192});
- `LT8` plaintext slots are the eight block values (L_j=f_{jmod 8}(x)) repeated across the physical slots;
- the source target before rotate-and-sum is (L_j y^{jmod 8}).

Use the two physical rows as different semantic lanes.

At stage (iin{0,1,2}), maintain one degree-one ciphertext (S_i) whose plaintext is

[
S_i =
igl[
A_i mid P_i
igr],
]

where:
- first row (A_i(j)) is the partially accumulated lower-polynomial term;
- second row (P_i(j)equiv y^{2^i}) is constant across that row.

Initialization:

[
A_0(j)=L_j,qquad P_0=y.
]

It is obtained linearly from the existing `LT8` and repeated (Y) ciphertexts by public row masks and addition.

Let (C_i(j)=((jmod 8)gg i)&1) and (D_i(j)=1-C_i(j)) on the first row. Let (R) denote the public selector for the second row.

Given (S_i=[A_imid P_i]), stock row swap gives

[
operatorname{RowSwap}(S_i)=[P_imid A_i].
]

Construct a degree-one factor ciphertext using only public-linear operations:

[
E_i
=
C_icdot operatorname{RowSwap}(S_i)
+
Rcdot S_i
+
[D_imid 0].
]

Therefore its plaintext is exactly

[
E_i=
igl[
D_i+C_iP_i mid P_i
igr].
]

Now perform exactly one scale-invariant ciphertext-ciphertext multiplication:

[
S_{i+1}=operatorname{SI}(S_i,E_i).
]

At the plaintext level,

[
A_{i+1}(j)
=
A_i(j)igl(D_i(j)+C_i(j)P_iigr),
]

and

[
P_{i+1}=P_i^2.
]

Inductively,

[
A_3(j)
=
L_jprod_{i=0}^{2}
left(D_i(j)+C_i(j)y^{2^i}ight)
=
L_j y^{jmod8},
]

while

[
P_3=y^8=x^{65536}.
]

Thus after three SI multiplications:
- the **first row is already the exact B175 pointwise target**;
- the **second row simultaneously contains the projected leading power** (x^{65536}).

No separate GROUPED ciphertext, terminal pointwise multiplication, or leading square is needed.

A turn-local exact modular simulator checked the recurrence for 100 random (xinmathbb Z_{65537}) and 100 random eight-block value vectors. Every first-row slot matched (L_j y^{jmod8}) and every second-row slot matched (y^8).

## Stock/source feasibility

Lattigo v6 source commit
`aacd8b2c0c2c900d3063a30b8290e255463e1bb9` provides every required primitive:
- `schemes/bgv/evaluator.go`, blob `8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f`: `RotateRows` is a degree-one Galois automorphism swapping the two batching rows; `MulRelinScaleInvariantNew` implements the fixed-level BFV-style SI multiplication used by B173/B174/B175.
- The same evaluator supports public vector/scalar plaintext multiplication and addition at the existing level.
- B158/B164-B174 already use the same row-rotation key type and scale-one public selector mechanism.

No new secret distribution, ring dimension, plaintext modulus, modulus chain, or evaluation-key type is required. The existing row-swap Galois key is reused.

Source/type gate: PASS_STATIC.

## Operation-count delta

Durable B175/B174 path after the 21-ctct checkpoint/basis prefix:

Current / projected terminal structure:
1. (Y^2) SI square;
2. (Y^4) SI square;
3. (F_0F_1) SI;
4. ((F_0F_1)F_2=mathrm{GROUPED}) SI;
5. (mathrm{LT8}	imesmathrm{GROUPED}) SI;
6. projected (Y^4	o Y^8=x^{65536}) leading square.

That is 6 terminal ct-ct operations and a projected full skeleton of

[
21+6=27.
]

The fused recurrence uses exactly 3 terminal SI multiplications and simultaneously emits both required outputs:

[
21+3=24.
]

So the optimistic ct-ct reduction is

[
27	o24,
]

i.e. 3 fewer ct-ct operations, about (11.1%) of the projected 27-ctct skeleton.

Costs added relative to the current terminal path:
- 3 row swaps / Galois key-switch operations;
- two public mask multiplications per stage to construct (E_i), plus a small number of row-isolation masks at input/output;
- public additions/constants.

No new Galois-key **type** is needed because the B158 basis already requires RowRotation. Exact runtime/RSS savings are NOT claimed.

## Fixed-Q value/noise ceiling

The semantic/count improvement does not by itself solve the audited failure.

Durable same-parameter evidence:
- B175 `LT8`: required bits (577), budget (+72);
- B174 SI accumulator multiplies add about (29)–(30) required bits over the noisier input;
- B175 terminal SI pointwise adds (31) required bits;
- B175 positive-output boundary is about (648) required bits at L18;
- B175 actual output required bits (664), budget (-15).

The fused construction puts the LT accumulator on a mandatory three-deep encrypted multiplication path. For a deliberately favorable value screen, grant:
- **zero** cost for every public mask, row swap, addition and packing operation;
- the **smallest observed comparable SI increment**, (29) required bits, for every fused SI multiplication;
- no extra penalty from the fact that the factor (E_i) is derived from the same noisy co-packed state;
- no extra component-lift/carry penalty.

Then the best calibrated recurrence is already

[
r_0=577,
qquad
r_1=577+29=606,
qquad
r_2=635,
qquad
r_3=664.
]

This is exactly in the already-audited B175 failure region and exceeds the positive fixed-Q threshold by about 16 bits.

The real construction is less favorable than this screen because each (E_i) is formed from masked/rotated copies of (S_i). B174 public masks cost about 16–17 required bits in the measured path, and the co-packed design re-couples the accumulator and power lane inside one RLWE ciphertext. No claim is made that those historical mask deltas are a formal lower bound here; they only make the zero-mask-cost screen intentionally optimistic.

The key paper-level point is therefore:

> Co-packing removes **operations**, but introduces no new source-backed tensor/reference error contraction. Under the smallest observed same-parameter SI growth, the required three encrypted multiplicative layers already consume all LT8 headroom.

A native run could only be justified by a **distinct** mechanism predicting materially smaller fused SI increments (roughly (le 23) bits on average to stay below 648 from 577), e.g. a proven covariance/carry cancellation. Packing alone supplies no such invariant.

Value gate: FAIL for the current fixed-Q paper claim.

This is a calibrated fixed-parameter value ceiling, not a universal theorem that every conceivable implementation of this algebraic recurrence must fail.

## Closest prior art / novelty boundary

Closest mechanisms:
1. the existing B158 co-packed EvalPower recurrence itself, which stores an accumulator and a binary power in two SIMD halves so one ct-ct multiplication updates both;
2. ordinary SIMD packing, Paterson-Stockmeyer polynomial evaluation, and shared/precomputed encrypted power bases;
3. generic circuit packing / layout optimization.

A bounded public search found standard PS power precomputation and SIMD packing, but no direct source matching the specific terminal recurrence that simultaneously:
- accumulates the three PS giant-power selector factors,
- advances (y	o y^2	o y^4	o y^8),
- returns both the lower-polynomial weighted output and the leading power after exactly three ct-ct operations.

However, because the construction is a direct transfer of the already-developed B158 co-packing principle to another stage of the same algorithm, **standalone novelty is not established**. At best it would strengthen a unified B158 paper contribution if the fixed-Q correctness/value gate could be solved.

`NOVELTY_STATUS=PREFLIGHT`, not CLEAR.

## Decision

`boot-b158-terminal-copacked-accumulator-power-fusion-v1` is **PARKED**.

Classification:

[
oxed{
	ext{PASS exact semantics}
/
	ext{PASS stock source}
/
	ext{FAIL calibrated fixed-Q value ceiling}
}
]

The operation-count mechanism is real and useful as an obstruction/architectural note, but it is not a credible fixed-Q paper candidate without a new noise/carry contraction mechanism.

### Reopen condition

Reopen only with concrete source-backed evidence that the fused co-packed SI recurrence has materially smaller tensor/reference growth than the existing 29–31-bit same-parameter SI operations, sufficient to keep all three fused stages and both final outputs below the fixed-Q correctness boundary with useful DFR.

The reopening package must also include:
1. exact L18 scale/carry semantics for all three co-packed multiplications;
2. same-parameter native whole-row correctness/noise traces;
3. complete final rotate-and-sum + leading-term semantics;
4. fair rotation/ct-pt/key/runtime/memory accounting;
5. independent novelty showing that terminal dual-output co-packing adds a publishable contribution beyond the already-known B158 recurrence.

Merely citing the 27->24 operation count, adding a Q prime, or assuming lower SI noise does not satisfy the reopen condition.

## Eliminated uncertainty

Whether the B158 co-packing trick can be transferred to the terminal PS merge to remove the failed B175 pointwise multiplication **and** the separate leading square while preserving exact semantics.

Answer:
- **Yes algebraically and in stock interfaces:** 6 terminal ct-ct operations collapse to 3, yielding a 27->24 projected full-skeleton count.
- **No as the current fixed-Q rescue:** the three-deep LT dependency reaches 664 required bits even under the zero-mask-cost / +29-bit-per-SI calibrated optimistic model, so operation fusion alone does not recover the missing fixed-Q margin.

## Evidence refs

- `findings/boot-B175-audit-direct-si-pointwise-noise-failure-2026-10-28.md`, blob `a9e8fe850c86a77717836ad414f8b6192290dd9a`.
- `findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md`, blob `ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29`.
- `findings/boot-B158-copacked-optimal-evalpower-2026-10-28.md`, blob `a956b5c3d5810f9b7ce2876c14e442270e7a53f2`.
- `findings/boot-B158-selector-norm-lift-layout-gate-2026-10-28.md`, blob `17fdf11bffe6044326fa243750d5b3869eb297f7`.
- Lattigo v6 `aacd8b2c0c2c900d3063a30b8290e255463e1bb9`, `schemes/bgv/evaluator.go` blob `8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f`.
- Turn-local exact modular recurrence check: 100 random (x) values and 100 random eight-block vectors, all slots exact.
- Bounded public prior-art search: ordinary PS encrypted-power precomputation and SIMD packing were found; no direct terminal dual-output co-packed recurrence was identified. This is not an independent novelty audit.
