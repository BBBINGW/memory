# BOOT RMFE Rank-5 Joint C2S + Correction Support Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 8/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This side-research turn tests one exact structural question independent of that task:

> On the actual post-RM10 active subspace, can the established 6-call R8 C2S map and the 4-call rank-5 shared correction map be synthesized jointly with fewer than 10 automorphism/key-switch calls?

No native execution, Codex resubmission, parameter change, source mutation, or heavy local task occurred.

## Fixed deterministic interface

Use the already-established plaintext algebra

\[
S=\mathbb Z/625\mathbb Z,\qquad
A=S[Y]/(Y^{16}+1),
\]

with two E8 slots and exact R8 C2S matrix \(L\) from the prior exact-map gate.

The desired post-C2S active slot subspace is

\[
V_{\rm act}
=
\operatorname{span}_S
\{e_0,\ldots,e_4,e_8,\ldots,e_{12}\}
\subset S^{16}.
\]

Let

\[
U=L^{-1}V_{\rm act}
\]

be the actual pre-C2S post-RM10 state space.

This is the correct restricted domain for joint synthesis.

## Automorphism action on the restricted domain

For \(u\in(\mathbb Z/32\mathbb Z)^*\), let \(P_u\) be the exact coefficient-basis automorphism

\[
Y^i\mapsto Y^{ui}\pmod{Y^{16}+1}.
\]

Conjugate into the C2S slot coordinates:

\[
A_u=L P_u L^{-1}.
\]

For the Frobenius-power support

\[
\mathcal S=
\{1,5,25,29,17\}
=
\{5^0,5^1,5^2,5^3,5^4\}\pmod{32},
\]

every \(A_u\) preserves the two E8 slots separately.

For either slot, restrict \(A_u\) to the five active input coordinates. The resulting \(5\times5\) response matrix is exactly

\[
R_{i,j}=Y^{i5^j},
\qquad 0\le i,j<5.
\]

Thus

\[
\boxed{R=M}
\]

where \(M\) is exactly the Moore matrix used in Turn 7.

The equality holds identically modulo 625 in both slots.

## Consequence: Turn-7 theta coefficients already implement the composite

Turn 7 solved

\[
D_t(Y^i)
=
\sum_{j=0}^{4}\theta_{t,j}Y^{i5^j}.
\]

Because the pre-C2S restricted response matrix is the same Moore matrix,

\[
(D_t\circ{\rm C2S})(x)
=
\sum_{j=0}^{4}\theta_{t,j}\sigma^j(x)
\qquad
\text{for every }x\in U.
\]

Therefore the same exact multipliers \(\theta_{t,j}\) from Turn 7 directly implement the **joint R8-C2S-plus-correction map**.

No separate 6-call R8 C2S stage is required on the restricted post-RM10 state.

Exact basis verification covers:

- 2 slots;
- 5 active basis vectors per slot;
- 4 outputs \(L_0,L_1,L_2,L_3\).

Total:

\[
2\times5\times4=40
\]

restricted-basis output checks, all exact modulo 625.

## Exact support lower bound

There are 16 automorphisms in \((\mathbb Z/32\mathbb Z)^*\).

Reduce the exact restricted action modulo 5 and test whether a chosen support spans the two required 5-dimensional selector subspaces.

All supports of sizes 1,2,3,4 were exhaustively tested:

\[
\binom{16}{1}
+\binom{16}{2}
+\binom{16}{3}
+\binom{16}{4}
=
2516
\]

candidate supports.

Result:

\[
\boxed{\text{none of the 2516 supports works}.}
\]

Size 5 is the first feasible support size. There are 56 feasible size-5 supports; 35 include the identity automorphism.

In particular,

\[
\{1,5,17,25,29\}
\]

is feasible.

Therefore the composite map requires at least five automorphism terms, and because one term is the identity:

\[
\boxed{4\text{ nonidentity automorphism/key-switch calls are minimal}}
\]

within the exact automorphism-multiplier family over the established R8 interface.

The impossibility is already visible modulo 5, so no mod-625 lift can rescue a 4-term support.

## Cost impact

Previous Turn-7 candidate transform count:

\[
5\;(\text{thin S2C})
+
10\;(\text{RM10})
+
6\;(\text{R8 C2S})
+
4\;(\text{shared correction})
=
25.
\]

Joint synthesis removes the separate R8 C2S:

\[
5+10+4
=
\boxed{19}.
\]

Against the five-branch baseline transform-side count 75:

\[
75\to19,
\]

a structural reduction of

\[
\boxed{74.67\%}.
\]

For the post-raw inverse/recovery side:

\[
70\to14,
\]

an exact structural reduction of

\[
\boxed{80.00\%}.
\]

The Turn-2 exact 5->1 boot-key reconstruction remains unchanged.

## Public-multiplier tax

Because the composite uses **the same exact \(\theta_{t,j}\)** as Turn 7, its HElib public-multiplier size is also exactly the Turn-7 result.

Worst correction output:

\[
\boxed{15.740880\text{ bits}}
\]

under the same optimistic triangle-bound HElib \`embeddingLargestCoeff\` ledger, excluding automorphism/key-switch noise.

The previously separate R8 C2S public-multiplier tax

\[
14.150203\text{ bits}
\]

is no longer sequentially incurred.

Thus the old conservative sequential public-multiplier-only bound

\[
14.150203+15.740880
=
29.891083\text{ bits}
\]

improves to

\[
\boxed{15.740880\text{ bits}}
\]

for the joint map.

This is not a whole-pipeline capacity result.

## Relation to prior negative results

This does not reopen the killed generic rank-16 direct-recovery route.

Turn 5 considered an arbitrary rank-16 input and found a generic four-output direct map cost of 15 automorphisms.

The present result depends critically on the actual restricted post-RM10 domain

\[
U=L^{-1}V_{\rm act},
\]

whose active rank is 5 per slot. The reduction is therefore a restricted-subspace synthesis, not a generic full-R8 transform.

It also does not contradict the killed cross-branch hoisting route: all four outputs here derive from one ciphertext and one shared Frobenius orbit.

## Verdict

\`\`\`text
RESULT:
  PASS_EXACT_JOINT_C2S_CORRECTION_SYNTHESIS

RESTRICTED_DOMAIN:
  U = C2S^{-1}(rank-5 active slot subspace)

EXACT_BASIS_CHECKS:
  40/40 PASS

MOORE_RESPONSE_IDENTITY:
  PRE-C2S restricted response matrix == Turn-7 Moore matrix

MIN_AUTOMORPHISM_TERMS:
  5

MIN_NONIDENTITY_AUTOMORPHISM_CALLS:
  4

SUPPORTS_SIZE_1_TO_4_TESTED:
  2516 / all FAIL

FEASIBLE_SIZE_5_SUPPORTS:
  56

SELECTED_SUPPORT:
  {1,5,17,25,29}

OLD_CANDIDATE_TRANSFORM_COUNT:
  25

NEW_CANDIDATE_TRANSFORM_COUNT:
  19

BASELINE_TRANSFORM_COUNT:
  75

STRUCTURAL_REDUCTION:
  74.67%

POST_RAW_RECOVERY_REDUCTION:
  70 -> 14 = 80.00%

WORST_PUBLIC_MULTIPLIER_TAX:
  15.740880 bits, excluding key-switch noise

SEPARATE_R8_C2S_STAGE:
  DOMINATED / REMOVE_FROM_CURRENT_CANDIDATE

NATIVE_LATENCY:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

NOVELTY:
  NOT ESTABLISHED
\`\`\`

## Pending native task interaction

The running baseline timer task remains valid and must not be rerun.

Its hard-kill threshold remains sufficient because the joint recovery still has positive cost.

If the baseline timing result passes, any later candidate implementation should use the 4-call joint map directly rather than the older 6+4 factorization.

## Next independent side-research

If the timer remains pending, the next highest-value static question is prior-art/novelty collision for the specific mechanism:

\[
\text{restricted post-rounding rank-5 subspace}
\to
\text{single boot-key reconstruction}
\to
\text{joint Moore/Frobenius recovery}.
\]

The high-level “one linear phase” direction is already disclosed by Aung et al.; the question is whether this exact post-rounding restricted-subspace mechanism appears in sparse/subring BGV bootstrapping or linear-transform literature.

AI_PROVISIONAL_CHOICE:
  RETAIN_POST_RAW_FUSION
  REPLACE_6_PLUS_4_RECOVERY_WITH_4_CALL_JOINT_MAP
  KEEP_PENDING_BASELINE_TIMER_AS_DECISIVE_LATENCY_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
