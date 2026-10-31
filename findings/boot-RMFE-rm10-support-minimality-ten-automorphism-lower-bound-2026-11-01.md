# BOOT RMFE RM10 Support-Minimality / Ten-Automorphism Lower-Bound Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 24/25
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

\`BBBINGW/memory main@d634f00ae5100cb5479b24d3d900a17b8b901c9c\`.

Relevant durable prerequisites:
- the p=5 subring-envelope candidate defines
  \[
  R=S[X]/(X^{16384}+1),\qquad
  S=\mathbb Z/625\mathbb Z,
  \]
  and
  \[
  R_8=S[Y]/(Y^{16}+1),\qquad Y=X^{1024};
  \]
- the post-inner-product coefficient-selection map is
  \[
  \mathrm{RM}_{10}=\mathrm{Tr}_{R/R_8},
  \]
  followed by multiplication by
  \[
  1024^{-1}\bmod625=224;
  \]
- Ma-style recursive realization uses
  \[
  \texttt{smartAutomorph}((m>>(i+1))+1),\quad i=0,\ldots,9,
  \]
  giving the ten targets
  \[
  16385,8193,4097,2049,1025,513,257,129,65,33;
  \]
- BSGS+10 makes each target a one-hop physical KeySwitch.

## Primary hypothesis

The current ten-call RM10 schedule may contain redundant automorphism stages and could perhaps be reduced below ten calls while preserving the exact coefficient-selection map using only:
- ciphertext copies;
- ciphertext additions/subtractions;
- multiplication by public ring constants;
- standard ring automorphisms.

Falsifier:
prove that RM10 has a unique automorphism-multiplier normal form with 1024 nonzero automorphism labels, while any such straight-line circuit using \(t\) automorphism gates can expose at most \(2^t\) labels.

## 1. The fixed subgroup of the embedded rank-16 subring

The outer cyclotomic automorphism group is

\[
G=(\mathbb Z/32768\mathbb Z)^*,
\]

with

\[
|G|=\phi(32768)=16384.
\]

An automorphism \(\sigma_u\) fixes

\[
Y=X^{1024}
\]

iff

\[
X^{1024u}=X^{1024}
\]

in the \(32768\)-th cyclotomic algebra, equivalently

\[
1024(u-1)\equiv0\pmod{32768}.
\]

Thus

\[
u\equiv1\pmod{32}.
\]

Define

\[
H=
\{
u\in G:u\equiv1\pmod{32}
\}.
\]

There are exactly

\[
\boxed{|H|=1024}
\]

such units.

The invariant subring has rank

\[
16384/1024=16
\]

over \(S\).

Since

\[
S[X^{1024}]/(X^{16384}+1)
\cong
S[Y]/(Y^{16}+1)
\]

already gives a rank-16 subring fixed by every \(u\in H\),

\[
\boxed{R^H=R_8.}
\]

## 2. RM10 is the normalized H-trace / Reynolds projector

The source-fixed RM10 coefficient-selection map is the relative trace:

\[
\operatorname{Tr}_{R/R_8}(x)
=
\sum_{h\in H}\sigma_h(x).
\]

Because \(5\nmid1024\), the group order is a unit in \(S\).

Indeed:

\[
1024\bmod625=399,
\]

and

\[
399^{-1}\bmod625=224.
\]

Hence the normalized map is

\[
\boxed{
P_H(x)
=
224\sum_{h\in H}\sigma_h(x).
}
\]

It is the Reynolds projector onto \(R^H=R_8\).

For an element already in \(R_8\),

\[
P_H(x)=x.
\]

For the source coefficient basis, this is exactly the established RM10 coefficient-selection behavior.

## 3. The ten source targets expand to all 1024 subgroup elements

Let

\[
u_i=(32768>>(i+1))+1,
\qquad i=0,\ldots,9.
\]

Explicitly:

\[
(u_0,\ldots,u_9)
=
(16385,8193,4097,2049,1025,513,257,129,65,33).
\]

Consider the recursive operator:

\[
T_{10}
=
\prod_{i=0}^{9}
(1+\sigma_{u_i}).
\]

Since \(G\) is abelian,

\[
T_{10}
=
\sum_{\epsilon\in\{0,1\}^{10}}
\sigma_{\prod_i u_i^{\epsilon_i}}.
\]

Exact modular enumeration gives prefix support sizes:

| stages used | newest target | distinct subset products |
|---:|---:|---:|
| 1 | 16385 | 2 |
| 2 | 8193 | 4 |
| 3 | 4097 | 8 |
| 4 | 2049 | 16 |
| 5 | 1025 | 32 |
| 6 | 513 | 64 |
| 7 | 257 | 128 |
| 8 | 129 | 256 |
| 9 | 65 | 512 |
| 10 | 33 | 1024 |

The final set is exactly:

\[
\boxed{
\left\{
\prod_i u_i^{\epsilon_i}\bmod32768:
\epsilon_i\in\{0,1\}
\right\}
=
\{1+32t:0\le t<1024\}
=
H.
}
\]

Thus every one of the \(2^{10}\) subset products is distinct.

Therefore:

\[
\boxed{
T_{10}
=
\sum_{h\in H}\sigma_h.
}
\]

Applying the final unit normalization gives:

\[
\boxed{
\mathrm{RM}_{10}
=
224\,T_{10}
=
P_H.
}
\]

So the ten-stage schedule is not heuristic clearing: it is an exact factorization of the 1024-term subgroup projector.

## 4. Uniqueness of automorphism-multiplier support

For a finite commutative Galois ring/algebra extension, the twisted/skew group algebra representation satisfies

\[
R\#G
\cong
\operatorname{End}_S(R).
\]

Equivalently, every \(S\)-linear endomorphism has a unique normal form

\[
L
=
\sum_{g\in G}a_g\sigma_g,
\qquad
a_g\in R.
\]

This is the same Galois-algebra principle already used in the R8 map-constructibility work.

For the projector \(P_H\),

\[
a_h=224
\]

for every \(h\in H\), and

\[
a_g=0
\]

for \(g\notin H\).

Since \(224\) is a unit modulo 625, all 1024 H-terms are genuinely nonzero.

Therefore:

\[
\boxed{
|\operatorname{supp}(P_H)|=1024
}
\]

in its unique automorphism-multiplier normal form.

No alternative public-multiplier coefficients can rewrite the same exact map with fewer automorphism labels inside this model.

## 5. Support-growth lemma for a straight-line linear circuit

Consider any circuit starting from one input ciphertext \(c\) and using only:

- copying;
- addition/subtraction;
- multiplication by arbitrary public ring constants;
- automorphism gates
  \[
  z\mapsto\sigma_u(z).
  \]

Represent every intermediate expression in normal form:

\[
z
=
\sum_{g\in G}a_g\sigma_g(c).
\]

Let \(S_t\) be the union of all automorphism labels that can occur in any expression after at most \(t\) automorphism-gate invocations.

Initially:

\[
S_0=\{1\}.
\]

Public multiplication changes only coefficients \(a_g\), not labels.

Addition/subtraction takes unions of existing supports and creates no new labels.

One new automorphism gate applied to an expression supported on \(S_t\) produces support

\[
uS_t.
\]

Hence the total global label set after that gate obeys:

\[
S_{t+1}
\subseteq
S_t\cup uS_t.
\]

Thus:

\[
|S_{t+1}|
\le
2|S_t|.
\]

By induction:

\[
\boxed{
|S_t|\le2^t.
}
\]

This bound allows:
- arbitrary reuse/copying of previous ciphertexts;
- arbitrary public multipliers;
- arbitrary additions;
- applying each automorphism to an already-large intermediate.

It is therefore stronger than a simple "one gate creates one term" count.

## 6. Exact lower bound

RM10 requires:

\[
|\operatorname{supp}(P_H)|=1024.
\]

Any permitted circuit using \(t\) automorphism gates satisfies:

\[
|\operatorname{supp}(L)|\le2^t.
\]

Therefore:

\[
2^t\ge1024=2^{10},
\]

so:

\[
\boxed{t\ge10.}
\]

The current recursive RM10 uses exactly ten automorphism gates.

Hence:

\[
\boxed{
t_{\min}=10.
}
\]

This is an exact support lower bound in the current linear automorphism-multiplier model.

## 7. Consequence for physical KeySwitch count

Each nontrivial ciphertext automorphism must be realized by at least one automorphism/evaluation-key application.

With the current BSGS+10 keyset, all ten RM10 target automorphisms are direct one-hop matrices.

Therefore current RM10 has:

\[
10
\]

physical KeySwitch applications.

The support lower bound gives:

\[
\boxed{
\text{RM10 physical KS}=10
}
\]

as minimal under the present standard HElib automorphism-key realization model.

Together with the independently support-minimal four-call joint rank-5 recovery:

\[
\boxed{
10+4=14
}
\]

is now structurally minimal for the current

\[
\mathrm{RM10}
\to
\text{joint rank-5 recovery}
\]

decomposition, subject to the stated model.

## 8. What this lower bound does not cover

It does not rule out a different primitive such as:

- a dedicated ring-switch / subring-extraction key;
- a new trace-specific evaluation key that is not a standard automorphism matrix;
- a representation in which the coefficient-selection projector is implicit;
- a cryptographically different secret/key relation;
- ciphertext-ciphertext nonlinear computation followed by cancellation;
- hardware/batched multi-output hoisting that reduces wall-clock cost without reducing automorphism support.

Such routes change the primitive or cost model.

They are not schedule improvements of the current standard automorphism-multiplier RM10.

## 9. Hoisting boundary

The lower bound is on required automorphism images / gates, not on:

- decomposition reuse;
- NTT reuse;
- cache locality;
- parallel execution;
- wall-clock latency.

A future implementation could make the ten required automorphisms cheaper through same-ciphertext hoisting while retaining all ten support labels.

That would be an implementation optimization, not a reduction in algebraic support.

No such task is started while the authorized native slot is occupied.

## 10. Implication for candidate reprioritization

Before this turn it remained plausible that RM10's ten calls were merely an unoptimized recursive schedule.

That possibility is now killed.

If the pending native result shows RM10 dominates latency, the next structural optimization should **not** search for a 9-call exact RM10 within the same automorphism-multiplier framework.

Reopen only if changing:
- primitive;
- representation;
- key relation;
- or exploiting implementation-level hoisting/parallelism.

## Verdict

\`\`\`text
RESULT:
  PASS_RM10_EXACT_SUPPORT_MINIMALITY
  FAIL_SUB10_AUTOMORPHISM_RM10_IN_CURRENT_LINEAR_MODEL

RM10_MAP:
  NORMALIZED RELATIVE TRACE / REYNOLDS PROJECTOR

FIXED SUBGROUP:
  H = {u mod 32768 : u == 1 mod 32}

H_SIZE:
  1024

RM10_NORMALIZATION:
  1024^{-1} mod 625 = 224

TEN_STAGE_SUBSET_PRODUCTS:
  EXACTLY H
  1024/1024 DISTINCT

RM10 UNIQUE AUTOMORPHISM SUPPORT:
  1024 NONZERO TERMS

SUPPORT_AFTER_t_AUTOMORPHISM_GATES:
  AT MOST 2^t

LOWER_BOUND:
  t >= log2(1024) = 10

CURRENT RM10 AUTOMORPHISM CALLS:
  10

CURRENT RM10 SUPPORT OPTIMALITY:
  EXACT / WITHIN MODEL

CURRENT BSGS+10 RM10 PHYSICAL KS:
  10
  MINIMAL WITH STANDARD AUTOMORPHISM-KEY REALIZATION

JOINT RECOVERY:
  4 NONIDENTITY CALLS
  INDEPENDENTLY SUPPORT-MINIMAL

CURRENT POST-RECONSTRUCTION 14-KS DECOMPOSITION:
  STRUCTURALLY MINIMAL
  WITHIN RM10 + JOINT LINEAR AUTOMORPHISM-MULTIPLIER MODEL

SUB-10 RM10 SCHEDULE SEARCH:
  KILL

REOPENING CONDITIONS:
  NEW PRIMITIVE / REPRESENTATION / KEY RELATION
  OR IMPLEMENTATION-LEVEL HOISTING THAT CHANGES COST, NOT SUPPORT

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

RM10's ten automorphism stages are not an implementation accident.

They realize the normalized 1024-element trace projector onto the rank-16 \(Y=X^{1024}\) invariant subring, and ten automorphism gates meet an exact \(2^t\)-support lower bound.

Therefore the current 10-call RM10 schedule is algebraically optimal inside the standard linear automorphism-multiplier framework. Any further reduction in this block requires changing the primitive or reducing per-gate cost rather than reducing the number of exact automorphism images.
