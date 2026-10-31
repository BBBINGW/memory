# BOOT RMFE Post-Rounding Delayed-Fusion Citation Closure

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 10/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn performs a citation-forward / citation-backward novelty closure on the one mechanism that survived Turn 9:

\[
\text{branchwise nonlinear rounding}
\to
\text{post-rounding common-bootkey delayed fusion}
\to
\text{restricted joint recovery}.
\]

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Primary question

Does later or adjacent BGV/BFV/slim/subring literature already contain the same semantic ordering:

1. preserve independently rounded branches;
2. only after branch-local rounding, merge them against a common encrypted boot key;
3. recover packed outputs by a sparse/restricted linear transform?

A positive match kills the surviving mechanism-level novelty.

## Chen-Han 2018: strongest collision on the broad architecture

Source:
Hao Chen and Kyoohyung Han,
*Homomorphic Lower Digits Removal and Improved FHE Bootstrapping*,
EUROCRYPT 2018 / ePrint 2018/067.

Their slim mode explicitly performs:

\[
\operatorname{Enc}(m_0,\ldots,m_{k-1})
\to
\text{InverseLinearTransformation}
\to
\operatorname{Enc}(m_0+m_1x^d+\cdots+m_{k-1}x^{d(k-1)})
\]

then

\[
\text{Modulus Switching + Dot Product with bootstrapping key}
\]

once on the packed polynomial, followed by a linear transform and one digit-extraction path.

Their Appendix A further exploits the fact that the coefficient plaintext is sparse. They decompose the return transform into:

- coefficient selection;
- a sparse linear transform of the form
  \[
  \sum_{i=0}^{k-1}\lambda_i\sigma_{s_i}(c),
  \]
  because only \(k\) coefficients are active.

Therefore Chen-Han already establishes both of the following broad principles:

1. multiple logical slot values can be moved into one sparse coefficient envelope and refreshed by a single modulus-switch / boot-key-dot-product path;
2. sparse post-bootstrap coefficient states can be returned to slots with only \(k\)-scale automorphism/plaintext-multiplier work.

This is a direct prior-art collision with any claim phrased as:

- "single MultKey for k packed values";
- "sparse coefficient envelope";
- "rank-k sparse recovery";
- "few-automorphism recovery from a sparse coefficient state".

## Geelen 2024/153: sparse/subring slot-to-coefficient transforms are systematic prior art

Source:
Robin Geelen,
*Revisiting the Slot-to-Coefficient Transformation for BGV and BFV*,
ePrint 2024/153.

The paper explicitly handles both fully and sparsely packed slots in power-of-two cyclotomics and develops FFT-like decompositions of SlotToCoeff/CoeffToSlot.

For sparsely packed slots, plaintexts live in a smaller subring. The transform can omit steps that act trivially on that subring and use traces/coefficient selection only where needed.

Thus the principle

\[
\text{actual plaintext lies in a lower-rank/subring state}
\Rightarrow
\text{replace ambient transform by a cheaper restricted transform}
\]

is established prior art.

Turn-6--8 rank-5 recovery cannot be claimed independently.

## Ma et al. 2024/164: thin/subring-specific simplification and transform fusion

Source:
Shihe Ma, Tairong Huang, Anyu Wang, Xiaoyun Wang,
*Faster BGV Bootstrapping for Power-of-Two Cyclotomics through Homomorphic NTT*,
ePrint 2024/164.

Their thin-bootstrapping optimizations explicitly exploit:

- integer-valued slots;
- subfield/subring structure;
- omission of transforms that are unnecessary on the restricted state;
- evaluation of some transforms on smaller subrings.

Therefore "restricted-state joint transform synthesis" is not a novelty axis by itself.

## Aung et al. 2025: the top-level direct-MultKey problem is already disclosed

Source:
Khin Mi Mi Aung et al.,
*Bootstrapping with RMFE for Fully Homomorphic Encryption*,
ePrint 2025/350 / PKC 2025.

Algorithm 2 performs \(k\) split MultKey paths.

Their conclusion explicitly states that it remains to be seen whether the MultKey portion can be done directly on RMFE-packed ciphertext to avoid repeated MultKey executions.

Therefore the research objective

\[
\text{direct RMFE-packed MultKey}
\]

is prior-disclosed.

## Search for post-rounding delayed merge

Targeted searches were performed around:

- "after modulus switching" + packed merge / common bootstrapping key;
- "independent modulus switching" + ciphertext merge;
- "post modulus switching" + coefficient-to-slot;
- HElib \`rawModSwitch\` / \`newMakeDivisible\`;
- subring/slim/restricted BGV bootstrapping;
- later survey and revisiting papers.

No direct source was found that uses the exact ordering:

\[
\boxed{
\text{independent branch rounding}
\to
\text{merge the rounded coefficient pairs}
\to
\text{one common encrypted-key reconstruction}
}
\]

for HElib/BGV-style recryption.

This is an absence-of-direct-collision result, not a proof of novelty.

## Why Chen-Han does not subsume the surviving mechanism

Chen-Han's slim mode deliberately packs the logical values **before** modulus switching:

\[
\text{slots}
\to
\text{sparse coefficient polynomial}
\to
\text{one ModSwitch + dot product}.
\]

The current RMFE redesign reached the opposite ordering only after a source-level obstruction was established:

- Aung/HElib branch semantics require branch-local \`rawModSwitch\`;
- \`newMakeDivisible\` chooses balanced representatives/carries branchwise;
- these operations are not linear and do not commute with the proposed pre-rounding RMFE envelope;
- therefore the obvious Chen-Han-style pre-pack route is not source-equivalent.

The surviving repair is:

1. keep all five branches separate through the nonlinear representative/carry boundary;
2. preserve the exact rounded public pairs \((a_i,b_i)\);
3. use the common encrypted recryption key \(K\) only after rounding:
   \[
   \sum_iY^i(a_i+b_iK)
   =
   \left(\sum_iY^ia_i\right)
   +
   \left(\sum_iY^ib_i\right)K;
   \]
4. then evaluate the restricted joint recovery.

That ordering is the only mechanism-level distinction still not directly collided by the sources checked in this turn.

## Novelty boundary after citation closure

\`\`\`text
SINGLE_MULTKEY_FOR_MULTIPLE_VALUES:
  PRIOR ART / CH18 + Aung future work

SPARSE_COEFFICIENT_ENVELOPE:
  PRIOR ART / CH18

SPARSE_K_TERM_AUTOMORPHISM_RECOVERY:
  PRIOR ART / CH18 Appendix A

SUBRING_OR_RESTRICTED_TRANSFORM:
  PRIOR ART / Geelen 2024/153 + Ma 2024/164

JOINT_LINEAR_TRANSFORM_FUSION:
  PRIOR ART PRINCIPLE

RANK5_MOORE_RECOVERY:
  TECHNIQUE TRANSFER / NOT STANDALONE NOVELTY

PRE-ROUNDING PACKED MULTKEY:
  PRIOR ART ARCHITECTURE / CH18

POST-ROUNDING COMMON-BOOTKEY DELAYED FUSION:
  NO DIRECT COLLISION FOUND IN TARGETED SEARCH

OBSTRUCTION_AWARE ORDERING:
  SURVIVING NARROW NOVELTY CANDIDATE

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED
\`\`\`

## Scientific interpretation

After Turn 10, the candidate should no longer be described as a new packed-bootstrapping transform.

The only defensible prospective contribution is an obstruction-and-repair statement:

> In the RMFE/HElib setting, the natural Chen-Han-style pre-rounding packing does not preserve the branchwise balanced representative/carry semantics. Delaying fusion until after the nonlinear rounding boundary restores exact semantics, after which existing sparse/restricted linear-transform techniques can recover the packed outputs efficiently.

Even this is not sufficient for a paper unless the pending native timing/capacity gates show a concrete frontier improvement.

## Decision

\`\`\`text
RESULT:
  PASS_CITATION_CLOSURE_NARROWS_CLAIM

DIRECT_PRIOR_ART_COLLISION_FOR_POSTROUND_DELAYED_FUSION:
  NOT FOUND

HIGH_LEVEL_AND_RECOVERY_TECHNIQUES:
  PRIOR ART COLLIDED

SURVIVING_CLAIM_TYPE:
  OBSTRUCTION + DELAYED-FUSION REPAIR

CANDIDATE_STATUS:
  RETAIN ONLY PENDING NATIVE VALUE

PENDING_BASELINE_TIMER:
  UNCHANGED / DO NOT RERUN

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Next independent side-research

If the timer remains pending, the highest-value static question is no longer novelty search on the same mechanism.

The next useful gate is to formalize the obstruction as a theorem-level commutation criterion:

- characterize exactly which public aggregation maps \(A\) commute with HElib \`rawModSwitch/newMakeDivisible\`;
- prove why the RMFE envelope fails that criterion;
- identify whether post-rounding fusion is the maximal exact fusion point.

A clean structural theorem would determine whether the surviving contribution has conceptual depth beyond an implementation-specific refactor.

AI_PROVISIONAL_CHOICE:
  RETAIN_POSTROUND_DELAYED_FUSION_PENDING_NATIVE_VALUE
  STOP_BROAD_NOVELTY_EXPANSION
  NEXT_STATIC_PRIORITY = COMMUTATION_CRITERION_THEOREM_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
