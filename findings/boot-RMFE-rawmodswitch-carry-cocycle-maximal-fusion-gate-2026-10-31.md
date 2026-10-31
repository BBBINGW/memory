# BOOT RMFE RawModSwitch / Carry-Cocycle Maximal-Fusion Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 11/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn formalizes the nonlinear commutation obstruction and determines the earliest exact branch-fusion point under the current HElib/Aung semantics.

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Primary hypothesis

The prior candidate narrative treated

\[
\text{rawModSwitch}
\to
\text{newMakeDivisible}
\to
/p^{e'}
\]

as one indivisible nonlinear boundary and fused only afterward.

This turn tests whether that boundary is truly maximal.

Falsifier:

- if \`newMakeDivisible\` has an explicit carry-defect formula that can be publicly corrected after branch aggregation, then fusion can move earlier;
- if branchwise \`rawModSwitch\` outputs cannot be recovered from an aggregate-only pre-raw state, then rawModSwitch remains the true irreducible boundary.

## Exact divisibility-lift map

Let

\[
P=p^{e'}
\]

and let

\[
q=p^e+1.
\]

Because \(e\ge e'\),

\[
q\equiv1\pmod P.
\]

Let

\[
\rho_P(z)\in\left[-\frac{P-1}{2},\frac{P-1}{2}\right]
\]

denote the centered representative of \(z\bmod P\).
Since \(P\) is odd, this representative is unique.

HElib's \`newMakeDivisible\` chooses the centered integer \(v\) satisfying

\[
z+vq\equiv0\pmod P.
\]

Since \(q\equiv1\pmod P\),

\[
v=-\rho_P(z).
\]

After division by \(P\), define the scalar map

\[
D_{P,q}(z)
=
\frac{z-q\rho_P(z)}{P}.
\]

This exactly models

\[
\text{newMakeDivisible}
\to
/p^{e'}
\]

coefficientwise.

## The carry-cocycle identity

Let \(a_1,\ldots,a_k\in\mathbb Z\) be public integer weights and \(z_1,\ldots,z_k\in\mathbb Z\).
Set

\[
s=\sum_i a_i z_i.
\]

Define

\[
\kappa_a(z_1,\ldots,z_k)
=
\frac{
\sum_i a_i\rho_P(z_i)-\rho_P(s)
}{P}.
\]

The numerator is divisible by \(P\), so \(\kappa_a\in\mathbb Z\).

Then

\[
\boxed{
D_{P,q}(s)
-
\sum_i a_iD_{P,q}(z_i)
=
q\,\kappa_a(z_1,\ldots,z_k)
}
\]

exactly.

Proof:

\[
D(s)-\sum_i a_iD(z_i)
=
\frac{
s-q\rho_P(s)
-\sum_i a_i z_i
+q\sum_i a_i\rho_P(z_i)
}{P}
\]

and \(s=\sum_i a_i z_i\), giving the result.

Thus the only obstruction to linearity of \`newMakeDivisible/divide\` is an explicit centered-residue carry cocycle.

## Exact commutation criterion

For a fixed aggregation row \(a=(a_1,\ldots,a_k)\),

\[
D\left(\sum_i a_i z_i\right)
=
\sum_i a_iD(z_i)
\]

if and only if

\[
\boxed{
\sum_i a_i\rho_P(z_i)
=
\rho_P\left(\sum_i a_i z_i\right)
}
\]

i.e. there is no centered-residue wrap/carry.

Therefore exact commutation is input-dependent.

### Universal integer-linear commutant

Suppose one requires the equality above for **all** integer inputs.

For odd \(P\ge3\), an integer row \(a\) commutes universally with \(D\) if and only if:

- every entry is zero except possibly one;
- the one nonzero entry, if present, is \(+1\) or \(-1\).

Sufficiency follows from

\[
\rho_P(\pm z)=\pm\rho_P(z).
\]

Necessity:

1. if one coefficient satisfies \(|a_i|\ge2\), choose a centered residue \(r\) with
   \[
   |a_i r|>(P-1)/2;
   \]
   then \(a_i\rho_P(z)\ne\rho_P(a_i z)\);

2. if at least two coefficients are nonzero, choose centered residues with signs matching the coefficients and magnitude \((P-1)/2\); their weighted sum leaves the centered interval, producing nonzero \(\kappa_a\).

Thus the universal commutant consists only of signed selectors / signed coordinate permutations.

## Application to the RMFE envelope

The candidate branch envelope is

\[
E(z_0,\ldots,z_4)
=
\sum_{i=0}^{4}Y^i z_i.
\]

Multiplication by each monomial \(Y^i\) is a signed coefficient permutation in the negacyclic outer ring.

But after summing the five shifted branches, every output coefficient is a signed sum of up to five independent input coefficients.

Therefore the aggregation matrix has rows with multiple nonzero \(\pm1\) entries and is **not** in the universal commutant of \(D\).

So the old statement

\[
D(E(z_i))=E(D(z_i))
\]

is false in general.

## But the carry defect is publicly correctable

After branchwise \`rawModSwitch\`, every \(z_i\) is already a public integer polynomial.

Hence the carry polynomial

\[
K
=
\frac{
\sum_iY^i\rho_P(z_i)
-
\rho_P\left(\sum_iY^i z_i\right)
}{P}
\]

is public and exactly computable coefficientwise.

The cocycle identity gives

\[
\boxed{
E(D(z_i))
=
D(E(z_i))-qK.
}
\]

Therefore one may:

1. execute branchwise \`rawModSwitch\` exactly as before;
2. aggregate the raw integer-polynomial outputs;
3. compute the public carry polynomial \(K\);
4. perform one aggregated divisibility-lift/divide;
5. subtract \(qK\);
6. continue with the single common-bootkey reconstruction.

This preserves the exact five-branch semantics.

### Carry magnitude for k=5

Each envelope output coefficient is a signed sum of five centered residues.

For unit weights \(\pm1\),

\[
|\kappa|\le2.
\]

Thus each carry correction coefficient is one of

\[
-2q,-q,0,q,2q.
\]

This is public integer arithmetic; it introduces no new encrypted secret term.

## Consequence: newMakeDivisible is not the irreducible boundary

The previous candidate delayed fusion until after

\[
\text{rawModSwitch}
+
\text{newMakeDivisible}
+
/P.
\]

That is more conservative than necessary.

The exact earliest branch-compression point currently established is:

\[
\boxed{
\text{immediately after branchwise rawModSwitch}
}
\]

provided the public carry cocycle is applied.

The branch-local \`newMakeDivisible/divide\` work need not remain five-way.

## Why rawModSwitch remains the true aggregate-only obstruction

Let \(R\) denote one coefficient of HElib \`rawModSwitch\`.

An exact aggregate-only pre-raw fusion would require a function \(G\) satisfying

\[
G(x+y)=R(x)+R(y)
\]

for all branch values.

Setting \(y=0\) and using \(R(0)=0\) forces

\[
G(x)=R(x).
\]

Hence

\[
R(x+y)=R(x)+R(y)
\]

for all \(x,y\): rawModSwitch would have to be additive.

But rawModSwitch selects bounded integer representatives after scale/round and plaintext-congruence correction. A nonzero map from the finite additive coefficient residue group to the torsion-free additive group of integers cannot be a group homomorphism.

Equivalently, the durable source-level witness already established:

\[
R(1)=1,\qquad
R(3)=3,\qquad
R(4)=-1
\]

for the pinned toy recurrence.

The two branch tuples

\[
(1,3)
\quad\text{and}\quad
(4,0)
\]

have the same aggregate input \(4\), but their desired branchwise raw outputs sum to

\[
4
\quad\text{versus}\quad
-1.
\]

Therefore no function of the aggregate input alone can reproduce the branchwise raw result.

This is stronger than simple noncommutativity: aggregate-only pre-raw compression loses information.

Randomized tie-breaking in HElib does not restore universal exact pathwise commutation; conditioning on any fixed tie-breaking tape leaves the same structural issue.

## Revised maximal-fusion statement

The strongest currently justified theorem-level statement is:

> For the current HElib/Aung branch semantics, any nontrivial aggregate-only linear compression performed before branchwise rawModSwitch cannot reproduce the exact sum of branchwise raw outputs for all inputs. After rawModSwitch, however, the remaining \`newMakeDivisible/divide\` nonlinearity is an explicit public carry cocycle and can be corrected exactly. Hence branchwise rawModSwitch is the earliest exact fusion boundary established without additional branch side information.

This is narrower and stronger than the previous "wait through rawModSwitch+newMakeDivisible" statement.

## Updated candidate pipeline

Current exact static candidate:

\[
5\times
\left(
\text{thin S2C}
\to
\text{reLinearize}
\to
\text{rawModSwitch}
\right)
\]

then

\[
\text{aggregate raw parts}
\to
\text{public carry correction}
\to
1\times\text{divisibility lift/divide}
\]

then

\[
1\times\text{common boot-key reconstruction}
\to
\text{RM10}
\to
\text{4-call joint restricted recovery}.
\]

The previously established transform count

\[
75\to19
\]

is unchanged because \`newMakeDivisible\` is public CPU arithmetic, not an automorphism/key-switch stage.

## Impact on the pending Turn-4 timer gate

The pending task itself remains useful and must not be modified or rerun.

However, the old decision rule

\[
\rho_{\rm ret}
=
\frac{
T_{\rm S2C}+T_{\rm preReconstruct}
}{
T_{\rm MultKey}
}
\ge0.5984704142
\Rightarrow
\text{KILL}
\]

is no longer formally valid as a hard lower bound.

Reason:

\`T_preReconstruct\` includes five-way

- \`newMakeDivisible\`;
- division by \(P\);

but these operations are no longer proven unavoidable five-way.

Thus the old \(\rho_{\rm ret}\) value remains a useful conservative measurement but cannot by itself kill the revised candidate unless the removable divisibility-lift share is separately bounded.

No task resubmission is needed.

## Novelty impact

Turn 10 narrowed the surviving novelty to obstruction-aware delayed fusion.

This turn sharpens that story:

- the \`newMakeDivisible\` obstruction is not fundamental;
- it is an explicit correctable carry cocycle;
- the genuine information-losing boundary is \`rawModSwitch\`;
- delayed fusion can move to immediately after rawModSwitch.

This provides a more conceptual obstruction/repair mechanism than the elementary post-divide linear identity alone.

It is still not a publishable contribution without concrete native value.

## Verdict

\`\`\`text
RESULT:
  PASS_RAWMODSWITCH_MAXIMAL_FUSION_THEOREM_GATE

NEWMakedIVISIBLE_NONLINEARITY:
  EXACT_PUBLIC_CARRY_COCYCLE

UNIVERSAL_COMMUTANT_OF_DIVISIBILITY_LIFT:
  SIGNED_SELECTORS ONLY

RMFE_ENVELOPE_COMMUTES_WITH_DIVISIBILITY_LIFT:
  NO, IN GENERAL

CARRY_COMPENSATED_POST_RAW_FUSION:
  PASS_EXACT

MAX_ESTABLISHED_FUSION_POINT:
  IMMEDIATELY_AFTER_BRANCHWISE_RAWMODSWITCH

PRE_RAW_AGGREGATE_ONLY_EXACT_FUSION:
  IMPOSSIBLE IN GENERAL

TRANSFORM_COUNT:
  75 -> 19 / unchanged

TURN4_OLD_HARD_KILL_RATIO:
  SUPERSEDED AS A FORMAL HARD LOWER BOUND

PENDING_NATIVE_TASK:
  UNCHANGED / DO_NOT_RERUN

NATIVE_LATENCY:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Next independent side-research

If the native timer is still pending, the next highest-value static question is whether a **compact auxiliary rounding-cocycle state** can cross rawModSwitch itself without reproducing all five branchwise raw conversions.

The cheapest first test should be an information/rank lower bound:

- characterize the rawModSwitch defect as a function of branch fractional/representative data;
- determine whether its exact correction requires branchwise information of dimension \(\Omega(k)\), or whether a lower-dimensional sufficient statistic exists.

If an \(\Omega(k)\) lower bound holds, the current post-raw boundary is not only aggregate-only maximal but work-compression maximal in a stronger sense.

AI_PROVISIONAL_CHOICE:
  RETAIN_REVISED_POST_RAW_FUSION
  MOVE_FUSION_POINT_TO_AFTER_RAWMODSWITCH_WITH_CARRY_COMPENSATION
  DO_NOT_APPLY_TURN4_HARD_KILL_RULE_BLINDLY

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
