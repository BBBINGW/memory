# BOOT RMFE Aggregate-Only Commutation / Carry-Cocycle Theorem Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 5/25
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

\`BBBINGW/memory main@a55349a44cb83471e2c8e82a57fef5c52fb5e128\`.

Relevant durable prerequisites:
- post-rounding delayed-fusion novelty collision gate;
- citation closure;
- rawModSwitch carry-cocycle/maximal-fusion gate;
- compact carry-state gate;
- rawModSwitch dataflow work-compression gate;
- current paired same-machine native-gate contract.

## Primary hypothesis

The surviving post-rounding mechanism may have conceptual depth beyond an implementation refactor if its obstruction can be promoted to a clean, general commutation theorem:

> nontrivial aggregate-only fusion across branch-local representative/rounding maps is impossible, while the following divisibility-lift nonlinearity differs from linearity by an explicit public carry cocycle.

Falsifier:
either the statement is false outside the exact HElib toy recurrence, or its mathematical core is already a standard carry/section-cocycle fact and therefore cannot itself support novelty.

## 1. Abstract aggregate-only obstruction

Let \(S\) be a finite abelian group and let

\[
R:S\to\mathbb Z
\]

be any deterministic nonzero map with \(R(0)=0\).

Consider one aggregation row with at least two signed unit coefficients

\[
\varepsilon_i\in\{-1,+1\}.
\]

Assume there exists an aggregate-only function

\[
F:S\to\mathbb Z
\]

such that for all branch inputs

\[
F\!\left(\sum_i \varepsilon_i x_i\right)
=
\sum_i\varepsilon_iR(x_i).
\]

Pick any nonzero coordinate \(i\), set all other inputs to zero, and write \(u=\varepsilon_i x_i\). Then

\[
F(u)=\varepsilon_iR(\varepsilon_i u).
\]

Now pick two nonzero coordinates \(i,j\). For arbitrary \(u,v\in S\), choose
\(x_i=\varepsilon_i u\), \(x_j=\varepsilon_j v\), all others zero. The assumed identity gives

\[
F(u+v)=F(u)+F(v).
\]

Therefore \(F:S\to\mathbb Z\) is a group homomorphism.

But \(S\) is finite and \(\mathbb Z\) is torsion-free, so every such homomorphism is zero:

\[
F=0.
\]

The single-coordinate identity then forces \(R=0\), contradicting the hypothesis.

Hence:

\[
\boxed{
\text{no nonzero finite-group representative map admits exact nontrivial signed aggregate-only fusion into }\mathbb Z.
}
\]

This theorem does not depend on HElib's exact rounding formula.

## 2. Application to HElib rawModSwitch

Fix the HElib tie-breaking tape, making coefficientwise \`rawModSwitch\` deterministic.

For one coefficient, the input is an element of the finite residue group determined by the current modulus \(Q\), while the exact branch output used by subsequent \`newMakeDivisible\` is a bounded integer representative.

Pinned HElib source:
\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`,
\`src/Ctxt.cpp:2941-3048\`.

The map is nonzero and sends zero to zero.

Each nontrivial RMFE envelope output coefficient is a signed sum of multiple branch coefficients because the public \(Y^i\) shifts are signed coefficient permutations followed by addition.

Therefore the abstract obstruction applies:

\[
\boxed{
\text{there is no exact function of the aggregate pre-raw coefficient alone that reproduces the sum of branchwise rawModSwitch integer representatives for all inputs.}
}
\]

This strengthens the earlier toy counterexample from an instance witness into a structural aggregate-only impossibility theorem.

Important boundary:
this is an impossibility for **aggregate-only exact compression with no branch-derived auxiliary state**.

It is NOT:
- an impossibility of streaming branchwise rounding;
- an \(\Omega(k)\) information lower bound;
- an asymptotic lower bound on RNS conversion work.

Turn 12 already established compact branch-derived carry state, so those stronger claims remain forbidden.

## 3. Post-raw divisibility map is a section-cocycle defect

Let \(P\ge3\) be odd, \(q\equiv1\pmod P\), and let

\[
\rho_P:\mathbb Z/P\mathbb Z\to
\left[-\frac{P-1}{2},\frac{P-1}{2}\right]
\]

be the balanced representative section.

Pinned \`newMakeDivisible\` adds the balanced multiple of \(q\) needed to make an integer divisible by \(P\). After division, define

\[
D_{P,q}(z)
=
\frac{z-q\rho_P(z)}{P}.
\]

For any integer aggregation row \(a=(a_1,\ldots,a_k)\), let

\[
s=\sum_i a_i z_i
\]

and

\[
\kappa_a(z_1,\ldots,z_k)
=
\frac{
\sum_i a_i\rho_P(z_i)-\rho_P(s)
}{P}.
\]

Because the numerator is divisible by \(P\),

\[
\kappa_a\in\mathbb Z.
\]

Direct expansion gives the exact commutator identity

\[
\boxed{
D_{P,q}(s)-\sum_i a_iD_{P,q}(z_i)
=
q\,\kappa_a(z_1,\ldots,z_k).
}
\]

Thus the post-raw divisibility map is not linear, but its failure of linearity is a completely explicit public carry.

## 4. Binary carry is a genuine 2-cocycle

For two residues define

\[
c_P(x,y)
=
\frac{
\rho_P(x)+\rho_P(y)-\rho_P(x+y)
}{P}.
\]

Associativity of integer addition gives

\[
c_P(x,y)+c_P(x+y,z)
=
c_P(y,z)+c_P(x,y+z).
\]

So \(c_P\) satisfies the ordinary 2-cocycle identity.

The weighted \(\kappa_a\) above is the corresponding multi-input carry obtained from the same section defect.

This mathematical phenomenon is classical, not new:
- carrying as a group-cohomology cocycle is established in the literature;
- balanced-digit carry processes are also established mathematical objects.

Therefore:

\[
\boxed{
\text{CARRY-COCYCLE MATHEMATICS ITSELF IS NOT A NOVELTY CLAIM.}
\]

## 5. Maximal exact fusion corollary for the current pipeline

The relevant branch pipeline is schematically

\[
\text{encrypted branch state}
\xrightarrow{R=\texttt{rawModSwitch}}
z_i\in\mathbb Z[X]
\xrightarrow{D=\texttt{newMakeDivisible}/P}
d_i
\xrightarrow{\operatorname{Rec}}
a_i+b_iK.
\]

Let \(E\) be the nontrivial signed RMFE envelope aggregation.

From Sections 1--2:

\[
\boxed{
E\text{ cannot be pushed before }R
}
\]

as an exact aggregate-only operation for all inputs.

From Sections 3--4:

\[
\boxed{
E\text{ can be pushed across }D
}
\]

after adding the explicitly computable public correction \(q\kappa\).

The common boot-key reconstruction is ring-linear after the two public channels are fixed, so it also commutes with \(E\).

Hence the precise structural boundary is:

> Under exact branch semantics and without retaining branch-derived auxiliary rounding state, branchwise \`rawModSwitch\` is the earliest exact fusion point. Once branchwise raw outputs exist, all remaining divisibility-lift nonlinearity is an explicit public carry cocycle, and the common reconstruction can be fused exactly.

With compact auxiliary carry state, branch raw outputs may be streamed/compressed, but the branch-local rounding decisions still have to be generated. Thus "post-raw is maximal" refers to semantic aggregate-only fusion, not necessarily to physical materialization or computational work.

## 6. Novelty consequence

The theorem gate separates three layers.

### Layer A — classical mathematics

- section defect / carrying is a 2-cocycle;
- balanced carries;
- finite-group-to-torsion-free homomorphism obstruction.

These are elementary/classical mathematics and should not be sold as new.

### Layer B — FHE-specific structural lemma

The new/useful application is the exact placement result:

\[
\text{pre-raw RMFE aggregation impossible aggregate-only}
\quad\text{but}\quad
\text{post-raw aggregation exact after public carry correction}.
\]

Targeted FHE searches found standard modulus-switch rounding-error analyses, but no direct source using this theorem to identify a maximal exact fusion boundary for independently rounded BGV/HElib bootstrap branches.

Absence of a direct match is not proof of novelty.

### Layer C — possible paper contribution

If the pending paired native gate gives a real frontier improvement, the defensible contribution story is:

1. natural packed/pre-rounding fusion is obstructed by branch-local representative selection;
2. the obstruction is structural, not an accidental code path;
3. the later divisibility nonlinearity is only a public carry cocycle;
4. delaying fusion exactly to that boundary preserves semantics;
5. the restricted recovery then yields measured systems value.

Without Item 5, this remains a correctness/architecture lemma around known mathematics, not a strong standalone contribution.

## Verdict

\`\`\`text
RESULT:
  PASS_STRUCTURAL_MAXIMAL_FUSION_LEMMA
  FAIL_NEW_GENERAL_CARRY_THEOREM_NOVELTY

AGGREGATE_ONLY_PRE_RAW_FUSION:
  IMPOSSIBLE FOR NONTRIVIAL SIGNED ROWS / GENERAL FINITE-TO-Z ARGUMENT

POST_RAW_DIVISIBILITY_FUSION:
  EXACT WITH PUBLIC CARRY-COCYCLE CORRECTION

RAW_MOD_SWITCH_BOUNDARY:
  EARLIEST EXACT AGGREGATE-ONLY FUSION POINT
  UNDER NO BRANCH-DERIVED AUXILIARY STATE

COMPACT_AUXILIARY_STATE:
  STILL POSSIBLE / TURN-12 RESULT PRESERVED

ASYMPTOTIC_RAW_WORK_LOWER_BOUND:
  NOT ESTABLISHED

CARRY_COCYCLE_MATHEMATICS:
  CLASSICAL / NOT NOVEL

FHE-SPECIFIC OBSTRUCTION-AND-REPAIR:
  POTENTIALLY USEFUL MECHANISM LEMMA
  NOVELTY NOT ESTABLISHED

CANDIDATE:
  RETAIN PENDING PAIRED NATIVE VALUE

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

PUBLISHABLE_NOVELTY:
  CONDITIONAL ON SYSTEMS VALUE + FINAL PRIOR-ART POSITIONING

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

This result reduces novelty risk in the right way: it gives a clean theorem-level explanation of why the candidate has its unusual ordering, but it also prevents overclaiming the underlying carry mathematics.

If the pending native task is strong, this lemma is suitable as the conceptual correctness/obstruction backbone of the mechanism.

If the pending task fails the systems-value gate, this theorem alone is not sufficient reason to keep the branch alive.
