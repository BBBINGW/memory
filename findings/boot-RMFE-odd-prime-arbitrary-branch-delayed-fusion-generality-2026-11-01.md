# BOOT RMFE Odd-Prime / Arbitrary-Branch Delayed-Fusion Generality Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 12/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@1063804966173f0396f5fd9251b9a876bf8778b0\`.

Relevant durable prerequisites:
- Turn 5 aggregate-only obstruction / carry-cocycle theorem;
- rawModSwitch carry-cocycle maximal-fusion gate;
- compact carry-state gate;
- exact common recrypt-key linear-form gate;
- Turn 11 novelty ceiling for joint recovery.

## Primary hypothesis

The surviving post-raw delayed-fusion mechanism may be only a \(p=5,k=5\) artifact.

Test whether the **fusion core itself** generalizes over the Aung/HElib odd-prime family:

\[
\text{branchwise rawModSwitch}
\to
\text{carry-corrected aggregate divisibility lift}
\to
\text{one common recryptEkey reconstruction},
\]

for arbitrary branch count \(k\) and public integer aggregation weights.

Falsifier:
find a dependence of the exact fusion identity on \(p=5\), \(k=5\), the specific modulus \(625\), or the rank-5 recovery map.

## Source provenance

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/recryption.cpp:69-136\`: \`newMakeDivisible\`;
- \`src/recryption.cpp:1035-1099\`: thin recryption rawModSwitch / two-part divisibility / common \`recryptEkey\` reconstruction;
- durable rawModSwitch source audit in \`src/Ctxt.cpp\`.

Aung et al. ePrint 2025/350 mirror:
- VERSION_UNVERIFIED;
- SHA256 \`922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82\`;
- physical p23 lists experimental primes
  \[
  3,5,7,11,13,53,59
  \]
  and RMFE dimensions \(w\in\{128,256,512,1024\}\);
- physical p25 gives correction-style examples
  \(p=3,k=7\),
  \(p=5,k=5\),
  \(p=11,k=5\).

All listed experimental primes are odd.

## 1. HElib divisibility lift is uniform over odd p

Set

\[
P=p^{e'}
\]

and

\[
q=p^e+1.
\]

HElib \`newMakeDivisible\` asserts

\[
q\bmod P=1.
\]

For odd \(p\), \(P\) is odd.

The source chooses, for each powerful-basis coefficient \(z\), the balanced integer \(v\) such that

\[
z+vq\equiv0\pmod P.
\]

The only randomized tie branch in \`newMakeDivisible\` is guarded by

\[
\texttt{p == 2}.
\]

Hence for every odd prime \(p\), the map is deterministic and the centered section

\[
\rho_P:\mathbb Z/P\mathbb Z
\to
\left[-\frac{P-1}{2},\frac{P-1}{2}\right]
\]

is unique.

With the sign convention used in the durable theorem,

\[
D_{P,q}(z)
=
\frac{z-q\rho_P(z)}{P}.
\]

Nothing in this formula depends specifically on \(p=5\) or \(P=625\).

## 2. Exact carry correction for arbitrary integer aggregation

Let public integer weights be

\[
a_1,\ldots,a_k\in\mathbb Z
\]

and let branch raw outputs in one active coefficient coordinate be

\[
z_1,\ldots,z_k\in\mathbb Z.
\]

Set

\[
s=\sum_{i=1}^k a_i z_i.
\]

Define

\[
\kappa_a
=
\frac{
\sum_i a_i\rho_P(z_i)
-
\rho_P(s)
}{P}.
\]

The numerator is divisible by \(P\), so

\[
\kappa_a\in\mathbb Z.
\]

Then exactly:

\[
\boxed{
D_{P,q}(s)
-
\sum_i a_iD_{P,q}(z_i)
=
q\kappa_a.
}
\]

Equivalently,

\[
\boxed{
\sum_i a_iD_{P,q}(z_i)
=
D_{P,q}\!\left(\sum_i a_i z_i\right)
-
q\kappa_a.
}
\]

This is valid for:
- any odd prime \(p\);
- any allowed \(e,e'\) with HElib's \(q\equiv1\pmod{P}\) condition;
- any branch count \(k\);
- any public integer weights.

Thus the fusion correction is not a \(p=5\) identity.

## 3. General carry magnitude

Let

\[
A=\sum_i |a_i|.
\]

Because every balanced residue satisfies

\[
|\rho_P(z_i)|\le\frac{P-1}{2}
\]

and

\[
|\rho_P(s)|\le\frac{P-1}{2},
\]

we have

\[
|\kappa_a|
<
\frac{A+1}{2}.
\]

Since \(\kappa_a\) is integral,

\[
\boxed{
|\kappa_a|\le\left\lfloor\frac{A}{2}\right\rfloor.
}
\]

For the RMFE envelope at one output coefficient, public monomial multiplication in the current power-of-two cyclotomic acts as a signed coefficient permutation, so the nonzero weights are \(\pm1\).

Hence if at most \(k\) branches contribute,

\[
A\le k
\]

and

\[
\boxed{
|\kappa|\le\left\lfloor\frac{k}{2}\right\rfloor.
}
\]

Examples:
- \(k=5\): \(|\kappa|\le2\);
- \(k=7\): \(|\kappa|\le3\).

Thus the public carry-state alphabet grows only linearly in \(k\), requiring \(O(\log k)\) bits per coefficient.

This generalizes the earlier \(k=5\) compact-carry result.

## 4. rawModSwitch remains the maximal aggregate-only boundary for all k

The Turn-5 finite-group-to-\(\mathbb Z\) obstruction did not use \(p=5\) or \(k=5\).

For any deterministic nonzero representative/rounding map

\[
R:S\to\mathbb Z
\]

from a finite additive residue group, a nontrivial aggregate-only exact fusion law with at least two active signed inputs would force \(R\) to be additive.

Every group homomorphism from finite \(S\) to torsion-free \(\mathbb Z\) is zero.

Therefore the pre-raw impossibility persists for arbitrary branch count:

\[
\boxed{
\text{nontrivial aggregate-only fusion cannot cross branchwise rawModSwitch}.
}
\]

The source \`rawModSwitch\` may randomize exact centered-\(q\) ties, including for odd \(p\) because \(q=p^e+1\) is even.

This does not affect the current mechanism:
- branchwise rawModSwitch is preserved;
- fusion starts only after the realized raw integer outputs exist;
- the carry correction is computed from those realized outputs.

So no independence or deterministic tie assumption is needed at this boundary.

## 5. Common recrypt-key reconstruction is k-independent

After carry-corrected divisibility processing, branch \(i\) has two public channels

\[
(a_i,b_i)
\]

corresponding to

\[
a_i+b_i s_R.
\]

Let \(T_i\) be the public ring-linear envelope operator for branch \(i\), e.g. the current monomial shift \(Y^i\).

Define

\[
A=\sum_i T_i(a_i),
\qquad
B=\sum_i T_i(b_i).
\]

All branches use the same HElib member \`recryptEkey\`.

For the common reconstruction operator

\[
\operatorname{Rec}(a,b)
=
b\cdot\texttt{recryptEkey}
+
a
\]

with HElib's common BGV constant-injection scale, public ring linearity gives

\[
\boxed{
\operatorname{Rec}(A,B)
=
\sum_i T_i\!\left(
\operatorname{Rec}(a_i,b_i)
\right).
}
\]

This identity is independent of:
- \(k\);
- \(p=5\);
- the RMFE rank;
- the downstream recovery map.

Therefore collapsing \(k\) stock reconstructions to one reconstruction is a general property of the common boot-key interface once branchwise raw decisions have been preserved.

## 6. General odd-prime fusion theorem for the Aung/HElib family

For the fixed HElib thin-recryption architecture and power-of-two cyclotomic setting used by Aung, assume:

1. \(p\) is odd;
2. every split branch is canonicalized to the same recryption-key basis;
3. branchwise \`rawModSwitch\` is performed exactly as stock;
4. the two public raw channels are kept typed separately;
5. branch aggregation is public ring-linear;
6. all branches reconstruct with the same \`recryptEkey\`.

Then for any branch count \(k\):

\[
\boxed{
\begin{aligned}
&k\text{ branch rawModSwitch decisions}\\
&\quad\to
\text{one aggregate divisibility lift}
+
\text{explicit public carry}\\
&\quad\to
\text{one common recryptEkey reconstruction}
\end{aligned}
}
\]

is exactly equivalent, at the secret-linear-form level, to performing the post-raw divisibility/reconstruction separately and then applying the same public aggregation.

So the **fusion core** is parameter-family general.

## 7. Direct relevance to Aung's experimental family

Aung's experimental prime set is

\[
\{3,5,7,11,13,53,59\},
\]

all odd.

Therefore every one of these primes satisfies the clean deterministic \`newMakeDivisible\` carry theorem above.

For the correction-style rows explicitly reported in Table 3:
- \(p=3,k=7\): carry magnitude at most 3;
- \(p=5,k=5\): carry magnitude at most 2;
- \(p=11,k=5\): carry magnitude at most 2.

Thus the mechanism is not inherently tied to the current \(p=5,k=5\) benchmark.

This does **not** establish that the current RM10/R8 recovery construction, latency advantage, capacity, or DFR generalizes to those other primes.

It establishes only the central nonlinear-boundary repair.

## 8. p=2 boundary

For \(p=2\), \(P=2^{e'}\) is even and HElib \`newMakeDivisible\` explicitly randomizes the exact half-residue tie.

A pathwise extension is plausible if the branch tie choices are treated as auxiliary state and the carry is defined using the realized selected representatives.

But the clean unique-section theorem above does not apply unchanged.

Therefore:

\[
\boxed{
p=2 \text{ is outside the currently established generality claim}.
}
\]

No p=2 novelty/performance claim is made.

This does not affect Aung's reported experimental family, which uses odd primes.

## 9. Novelty / importance consequence

Turn 11 established that joint recovery is mostly prior-art linear-map machinery.

This turn strengthens the remaining central mechanism in the opposite dimension:

the nonlinear obstruction-and-repair is **not** merely an instance-specific \(p=5\) patch.

The defensible prospective contribution can be stated at the family level:

> For odd-prime HElib/BGV thin-recryption branches, aggregate-only fusion is structurally blocked by branchwise raw representative selection. Once those raw decisions are preserved, the subsequent divisibility defect is an explicit bounded public carry and all branch reconstructions against the common boot key can be fused exactly.

This is broader than the native benchmark regime.

But publishability still requires a concrete regime in which the generalized mechanism yields useful systems value.

## Verdict

\`\`\`text
RESULT:
  PASS_ODD_PRIME_ARBITRARY_BRANCH_FUSION_GENERALITY

FUSION_CORE_DEPENDS_ON_P_EQUALS_5:
  NO

FUSION_CORE_DEPENDS_ON_K_EQUALS_5:
  NO

ODD_P_NEWMakedivisible:
  DETERMINISTIC UNIQUE BALANCED SECTION

GENERAL_CARRY_IDENTITY:
  sum_i a_i D(z_i)
  =
  D(sum_i a_i z_i) - q*kappa_a

GENERAL_CARRY_BOUND:
  |kappa_a| <= floor((sum_i |a_i|)/2)

RMFE_SIGNED_ENVELOPE_BOUND:
  |kappa| <= floor(k/2)

RAW_MOD_SWITCH_PRE-FUSION_OBSTRUCTION:
  GENERAL / NOT P=5 SPECIFIC

COMMON_RECRYPTEKEY_RECONSTRUCTION:
  K-INDEPENDENT LINEAR IDENTITY

AUNG_ODD_PRIME_FAMILY:
  {3,5,7,11,13,53,59}
  FUSION SEMANTICS COVERED

P_EQUALS_2:
  NOT INCLUDED IN CLEAN THEOREM
  RANDOM HALF-TIE NEEDS SEPARATE ANALYSIS

P5_RM10_RANK5_RECOVERY_GENERALIZES:
  NOT ESTABLISHED

OTHER-PRIME PERFORMANCE:
  NOT ESTABLISHED

OTHER-PRIME DFR:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  STILL CONDITIONAL ON SYSTEMS FRONTIER MOVEMENT
  BUT CENTRAL MECHANISM IS FAMILY-GENERAL, NOT INSTANCE-ONLY

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The current \(p=5,k=5\) native task remains the correct decisive systems gate.

If it passes, the mechanism can be presented as an odd-prime family-level obstruction-and-repair with \(p=5\) as the implemented validation point, rather than as a one-off algebraic trick.

Do not claim that the current RM10/rank-5 recovery or throughput result automatically transfers to other primes.
