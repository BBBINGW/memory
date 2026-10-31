# BOOT RMFE RawModSwitch Compact Carry-State Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 12/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn tests the Turn-11 reopening condition:

> Does exact fusion across branchwise \`rawModSwitch\` require \(\Omega(k)\) branchwise information, or is there a compact auxiliary rounding state that preserves exact semantics?

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Coefficient-level rawModSwitch model

Fix one powerful-basis coefficient.

Let:

- \(Q\) be the current ciphertext modulus;
- \(q=p^e+1\) be the HElib recryption modulus;
- \(P=p^r\) be the current plaintext space (\`ptxtSpace\`).

For branch coefficient \(c_i\), using its canonical centered integer representative, HElib computes:

\[
x_i=\operatorname{Round}\!\left(\frac{q c_i}{Q}\right),
\]

\[
y_i=q c_i-Qx_i,
\]

where \(y_i\) is the centered residual.

It then computes the centered plaintext-correction residue

\[
\delta_i
=
\rho_P\!\left(y_iQ^{-1}\bmod P\right),
\]

forms

\[
u_i=x_i+\delta_i,
\]

and finally centers modulo \(q\):

\[
r_i=u_i-q t_i.
\]

Here \(t_i\in\{-1,0,1\}\) for the current HElib regime \(q>P\), after fixing the tie-breaking tape.

The branch raw output is \(r_i\).

## Signed branch aggregation

For one output coefficient of the RMFE \(Y^i\)-envelope, the branch weights are signed selectors

\[
a_i\in\{-1,+1\}.
\]

Let

\[
A=\sum_i|a_i|.
\]

For the current \(k=5\) envelope, \(A=5\).

Let the integer branch sum be

\[
s=\sum_i a_i c_i.
\]

The aggregate ciphertext coefficient is represented modulo \(Q\) by

\[
c=\rho_Q(s),
\]

and define the \(Q\)-wrap carry

\[
h=\frac{s-c}{Q}\in\mathbb Z.
\]

Apply the same rawModSwitch scalar logic to \(c\), producing

\[
x,y,\delta,u,r,t.
\]

## First carry: scale-round discrepancy

Define

\[
\alpha
=
\sum_i a_i x_i-x-hq.
\]

Because

\[
s=c+hQ,
\]

and rounding commutes with integer shifts,

\[
\alpha\in\mathbb Z.
\]

Moreover the residuals satisfy the exact identity

\[
\sum_i a_i y_i
=
y-Q\alpha.
\]

Since every nearest-rounding error has magnitude below \(1/2\),

\[
|\alpha|<\frac{A+1}{2}.
\]

## Second carry: plaintext-correction discrepancy

Because

\[
\delta_i
\equiv
y_iQ^{-1}
\pmod P,
\]

the residual identity implies

\[
\sum_i a_i\delta_i
\equiv
\delta-\alpha
\pmod P.
\]

Therefore define the exact integer carry

\[
\boxed{
\kappa_P
=
\frac{
\sum_i a_i\delta_i-\delta+\alpha
}{P}.
}
\]

Then

\[
\sum_i a_i\delta_i
=
\delta-\alpha+P\kappa_P.
\]

Combining with the \(x_i\) terms yields a cancellation of the scale-round carry:

\[
\boxed{
\sum_i a_i u_i
=
u+hq+P\kappa_P.
}
\]

Thus the intermediate rounding discrepancy \(\alpha\) does not need to be retained separately.

For general signed \(A\)-way aggregation,

\[
|\kappa_P|<\frac{A+1}{2}.
\]

For \(A=5\),

\[
\boxed{
\kappa_P\in\{-2,-1,0,1,2\}.
}
\]

## Third/final carry: centered-q representative discrepancy

Recall

\[
r_i=u_i-q t_i,
\qquad
r=u-qt.
\]

Define

\[
\boxed{
\kappa_q
=
h+t-\sum_i a_i t_i.
}
\]

Then

\[
\boxed{
\sum_i a_i r_i
=
r+P\kappa_P+q\kappa_q.
}
\]

This is the exact rawModSwitch branch-fusion defect formula.

For the current \(A=5\):

- \(|h|\le2\);
- \(t,t_i\in\{-1,0,1\}\).

Hence the conservative bound is

\[
\boxed{
|\kappa_q|\le8.
}
\]

So each output coefficient needs only:

\[
\kappa_P\in[-2,2],
\qquad
\kappa_q\in[-8,8].
\]

That is at most

\[
5\times17=85
\]

carry states, i.e. at most 7 bits of auxiliary state per coefficient under this conservative bound.

## Main information-theoretic consequence

The exact branchwise raw outputs do **not** require retaining \(k\) full integers once the aggregate raw output is known.

They are determined by:

1. one aggregate raw output coefficient \(r\);
2. one small plaintext-residue carry \(\kappa_P\);
3. one small centered-\(q\) carry \(\kappa_q\).

Therefore the Turn-11 proposed \(\Omega(k)\) information lower bound is false.

The auxiliary state per coefficient is \(O(\log k)\) bits for fixed \(P,q\), not \(\Omega(k)\) branch values.

This is a statement about information dimension, not computational cost.

## Relation to the durable rawModSwitch counterexample

The existing source-shaped witness has

\[
R(1)=1,\qquad
R(3)=3,\qquad
R(4)=-1,\qquad
R(0)=0.
\]

Thus two branch tuples

\[
(1,3)
\quad\text{and}\quad
(4,0)
\]

have the same aggregate input \(4\) but different raw sums

\[
4
\quad\text{versus}\quad
-1.
\]

This still proves Turn 11's result:

\[
\text{aggregate input alone is insufficient}.
\]

Turn 12 explains exactly what extra information is missing: a compact carry state.

There is no contradiction.

## Revised fusion interpretation

The semantic boundary is now:

- branchwise **rounding decisions** \(x_i,\delta_i,t_i\) remain necessary;
- five fully materialized raw output polynomials are not information-theoretically necessary.

A source-faithful implementation could, in principle:

1. perform each branch's DCRT-to-powerful conversion and per-coefficient rounding logic;
2. accumulate only:
   - aggregate raw state,
   - \(\kappa_P\) polynomial,
   - \(\kappa_q\) polynomial;
3. materialize only the aggregate polynomial needed by the later carry-compensated divisibility lift / common boot-key reconstruction.

This may avoid some branch-local output conversion/materialization work.

However, the current derivation does **not** show that the expensive branchwise \`dcrtToPowerful\` conversion can be avoided.

## Computational boundary

The two carries depend on branch-local internal quantities:

\[
x_i,\delta_i,t_i.
\]

Those quantities are nonlinear representative/rounding decisions.

Therefore a compact state exists, but computing it may still require essentially the same per-branch coefficient inspection as rawModSwitch.

No runtime saving is claimed.

In particular:

\[
\boxed{
\text{information compression}
\ne
\text{work compression}.
}
\]

## Impact on the pending timer task

The running Turn-4 timer task remains useful and must not be modified or rerun.

Turn 11 already superseded its original hard-kill ratio because five-way \`newMakeDivisible/divide\` is removable.

Turn 12 adds another interpretation:

- if rawModSwitch timing is dominated by branchwise DCRT-to-powerful conversion, the compact-carry result may provide little speedup;
- if a material fraction comes from branch-local output conversion/materialization, that part may be compressible.

The timer result should therefore be audited at source-substage granularity before any revised kill rule is applied.

## Verdict

\`\`\`text
RESULT:
  PASS_COMPACT_RAWMODSWITCH_CARRY_STATE

OMEGA_K_INFORMATION_LOWER_BOUND:
  FAIL

AGGREGATE_ONLY_RAW_FUSION:
  STILL IMPOSSIBLE

EXACT_AUXILIARY_STATE:
  TWO SMALL INTEGER CARRIES PER COEFFICIENT

RAW_DEFECT_FORMULA:
  sum_i a_i R(c_i)
  =
  R(aggregate)
  + P*kappa_P
  + q*kappa_q

CURRENT_K5_KAPPA_P:
  {-2,-1,0,1,2}

CURRENT_K5_KAPPA_Q:
  subset of [-8,8]

AUXILIARY_STATE_SIZE:
  <= 7 bits/coefficient under conservative bounds

FULL_BRANCH_RAW_OUTPUT_MATERIALIZATION:
  NOT INFORMATION-THEORETICALLY NECESSARY

BRANCHWISE_ROUNDING_DECISION_EXTRACTION:
  STILL NECESSARY / WORK LOWER BOUND NOT ESTABLISHED

NATIVE_SPEEDUP:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Next independent side-research

If the native timer remains pending, the highest-value source-level question is now computational rather than informational:

> Which exact substeps of HElib \`rawModSwitch\` remain \(k\)-way if only the aggregate raw polynomial plus \(\kappa_P,\kappa_q\) are required?

The cheapest gate is a static source dataflow audit of:

- \`PowerfulDCRT::dcrtToPowerful\`;
- the coefficient rounding loop;
- \`powerfulToZZX\`;
- branch-local allocation/copying.

Goal:

- prove which conversions can be reduced from \(5\to1\);
- identify a revised static latency ceiling without running a second native task.

AI_PROVISIONAL_CHOICE:
  RETAIN_COMPACT_CARRY_STATE
  ABANDON_OMEGA_K_INFORMATION_LOWER_BOUND
  NEXT_STATIC_PRIORITY = RAWMODSWITCH_DATAFLOW_WORK_COMPRESSION_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
