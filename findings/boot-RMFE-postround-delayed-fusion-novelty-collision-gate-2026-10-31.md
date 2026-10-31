# BOOT RMFE Post-Rounding Delayed-Fusion Novelty Collision Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 9/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn performs one targeted prior-art/novelty audit for the current exact mechanism:

\[
\text{branchwise nonlinear rounding}
\to
\text{common boot-key reconstruction}
\to
\text{restricted rank-5 joint Moore/Frobenius recovery}.
\]

No native execution, source modification, Codex resubmission, or new performance claim occurred.

## Primary hypothesis

The current candidate may retain a narrow mechanism-level novelty even though the high-level objective "do MultKey once on packed data" and the linear-transform machinery are heavily prior-art-collided.

Falsifier:

- a prior work already performs the same branchwise nonlinear ModSwitch/carry step separately,
- then algebraically fuses the post-rounding coefficient pairs against one common boot key,
- and directly recovers packed/correction outputs from the resulting restricted state.

If such a source exists, the current mechanism is not novel.

## Collision matrix

### 1. Halevi-Shoup 2018 — linearized-polynomial / Frobenius maps

Source:
Halevi and Shoup, *Faster Homomorphic Linear Transformations in HElib*, ePrint 2018/244.

Established prior-art principle:

For a degree-d Galois-ring slot E, every base-ring-linear map can be written uniquely as

\[
M(\eta)=\sum_{j=0}^{d-1}\lambda_j\sigma^j(\eta),
\]

and evaluated homomorphically using Frobenius automorphisms and plaintext constants.

Collision with current work:

- Moore/Frobenius representation itself;
- computing exact linear maps on a restricted slot submodule;
- sharing Frobenius orbit ciphertexts among multiple outputs.

Therefore none of these is a standalone novelty claim.

### 2. FIMD 2022 — arbitrary RMFE component-linear maps folded into recode

Source:
Aung et al., *Field Instruction Multiple Data*, ePrint 2022/771 / EUROCRYPT 2022.

Prior-art principle:

For an RMFE-packed vector, arbitrary component-wise linear maps
\[
\tau:(\mathbb F_q)^k\to(\mathbb F_q)^k
\]
can be sandwiched as
\[
\phi\circ\tau\circ\psi
\]
and folded into the FHE recode operation, including after homomorphic multiplication.

Collision:

- using RMFE linearity to realize correction/recovery maps;
- folding an RMFE component-linear transformation into an already-required linear phase.

Thus "joint correction-map evaluation" or "free linear map during recovery" is not enough for novelty.

### 3. Chen-Han 2018 — slim bootstrapping performs one packed ModSwitch + boot-key dot product

Source:
Chen and Han, *Homomorphic Lower Digits Removal and Improved FHE Bootstrapping*, ePrint 2018/067 / EUROCRYPT 2018.

Their slim workflow for a plaintext subspace
\[
\mathbb Z_{p^r}^k
\]
is:

\[
\text{batched slots}
\to
\text{inverse linear transform}
\to
m_0+m_1x^d+\cdots+m_{k-1}x^{d(k-1)}
\to
\text{one Modulus Switching + boot-key dot product}
\to
\text{linear transform}
\to
\text{one Digit Extraction}.
\]

This is a serious collision.

It establishes prior art for the broad idea:

> pack multiple logical values into polynomial coefficients before bootstrapping so that one boot-key dot product refreshes all of them.

Therefore the current work cannot claim novelty for:

- "single MultKey for multiple logical components";
- "coefficient envelope around one boot-key inner product";
- "packed subspace bootstrapping with one digit-extraction path".

### 4. Ma et al. 2024 — exploit restricted thin/subring states and fuse linear maps

Source:
Ma et al., *Faster BGV Bootstrapping for Power-of-Two Cyclotomics through Homomorphic NTT*, ePrint 2024/164.

Prior-art principles include:

- in thin bootstrapping, some sub-transforms can be omitted because inputs lie in the integer subring;
- other transforms can be evaluated over a smaller slot subring;
- an extra linearized polynomial map can be incorporated into the last BlockMatMul1D stage "for free";
- CoeffToSlot / SlotToCoeff are optimized based on the actual intermediate subring.

Collision:

- exploiting a restricted active subspace/subring to lower automorphism cost;
- jointly synthesizing adjacent linear transforms;
- avoiding a full ambient-rank transform when the actual state has smaller algebraic rank.

Thus Turn-6/7/8 rank-5 restriction and joint C2S/correction synthesis are optimization mechanisms, not independent novelty.

### 5. Peikert-Pepin 2025 — sparse automorphism decompositions for packed bootstrapping

Source:
Peikert and Pepin, *Vive Galois! Part 1: Optimal SIMD Packing and Packed Bootstrapping for FHE*, 2025.

Their framework explicitly separates:

- homomorphic structured CRT transforms, expressed sparsely through automorphisms;
- the nonlinear rounding/noise-removal part of packed bootstrapping.

It gives a general sparse-decomposition framework for structured linear transforms in abelian number rings/subfields.

Collision:

- sparse automorphism synthesis of packed-bootstrapping linear transforms;
- structured subfield/subring packed bootstrapping as a general concept.

It does not directly expose the current HElib RMFE post-rounding fusion identity.

### 6. Aung et al. 2025 — direct RMFE-packed MultKey is explicit future work

Source:
Aung et al., *Bootstrapping with RMFE for Fully Homomorphic Encryption*, ePrint 2025/350 / PKC 2025.

Their Algorithm 2 executes:

\[
\text{SlotsToCtxts}
\to
k\times(\text{ModSwitch, SlotsToCoeff, InnerProduct, CoeffToSlots})
\to
\text{CtxtsToSlots}.
\]

The conclusion explicitly states as future work that it remains to be seen whether the MultKey portion can be done directly on RMFE-packed ciphertext to avoid executing MultKey multiple times on split ciphertexts.

Therefore:

\[
\boxed{\text{HIGH-LEVEL DIRECT-MULTKEY PROBLEM NOVELTY = KILLED}}
\]

The research problem is prior-disclosed.

## Surviving narrow mechanism

Targeted search did **not** identify a direct prior-art match for the following exact sequence:

1. preserve Aung's branch-specific thin processing through the nonlinear
   \[
   \text{rawModSwitch}+\text{newMakeDivisible}+/p^{e'}
   \]
   boundary;

2. after each branch has committed its own balanced carry/rounding choice, write
   \[
   B_i=a_i+b_iK
   \]
   for the common HElib encrypted recryption key K;

3. aggregate only after rounding:
   \[
   A=\sum_iY^i a_i,\qquad
   B=\sum_iY^i b_i,
   \]
   and reconstruct once:
   \[
   A+BK=\sum_iY^i(a_i+b_iK);
   \]

4. exploit the resulting restricted rank-5 post-rounding state to evaluate all correction outputs through one jointly synthesized Frobenius map.

This differs from Chen-Han slim bootstrapping in a material way:

Chen-Han packs the plaintext-slot values **before** modulus switching and intentionally performs one packed modulus-switch/dot-product path.

The current mechanism was developed only after exact audit showed that, for the HElib/Aung branch semantics, the branchwise
\[
\text{rawModSwitch/newMakeDivisible}
\]
representative choices do not commute with the proposed pre-rounding RMFE envelope.

The candidate therefore does not claim that pre-rounding packing is new. Its distinctive mechanism is:

\[
\boxed{
\text{delay fusion until after the nonlinear carry/rounding boundary}
}
\]

so the five branch-specific rounding decisions are preserved exactly while the common encrypted-key reconstruction is still collapsed from 5 to 1.

## Novelty disposition

\`\`\`text
HIGH_LEVEL_SINGLE_MULTKEY:
  KILLED / PRIOR-DISCLOSED by Aung 2025

PACK_BEFORE_MODSWITCH_AND_ONE_BOOTKEY_DOT_PRODUCT:
  PRIOR ART / Chen-Han 2018

FROBENIUS_OR_MOORE_LINEAR_MAP:
  PRIOR ART / Halevi-Shoup 2018

RMFE_COMPONENT_LINEAR_MAP_FOLDING:
  PRIOR ART / FIMD 2022

RESTRICTED_SUBRING_LINEAR_TRANSFORM:
  PRIOR ART / Ma 2024

JOINT_LINEAR_TRANSFORM_FUSION:
  PRIOR ART PRINCIPLE / Ma 2024 + structured-transform literature

SPARSE_AUTOMORPHISM_PACKED_BOOTSTRAPPING:
  PRIOR ART FRAMEWORK / Peikert-Pepin 2025

POST-ROUNDING COMMON-BOOTKEY DELAYED FUSION:
  NO DIRECT COLLISION FOUND IN TARGETED SEARCH

POST-ROUNDING FUSION + RESTRICTED JOINT CORRECTION RECOVERY:
  NARROW NOVELTY CANDIDATE / NOT ESTABLISHED
\`\`\`

## Technical-nontriviality assessment

The surviving algebraic identity

\[
\sum_iY^i(a_i+b_iK)
=
\left(\sum_iY^i a_i\right)
+
\left(\sum_iY^i b_i\right)K
\]

is itself elementary.

Therefore a paper cannot be based on that identity alone.

Potential technical value must come from the full obstruction-and-repair story:

1. the obvious Chen-Han-style/pre-rounding packing route collides with the HElib/Aung nonlinear representative/carry semantics;
2. exact pre-rounding branch-equivalence fails;
3. delaying fusion until after the nonlinear boundary restores exact branch semantics;
4. the post-rounding restricted state admits a minimal 4-call joint correction map;
5. native latency/capacity must show that this boundary-aware repair moves the throughput frontier.

Without Item 5, the mechanism is likely too close to a source-level algebraic refactor for a strong standalone contribution.

## Decision

\`\`\`text
RESULT:
  PASS_NARROW_NOVELTY_BOUNDARY_IDENTIFIED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

NOVELTY_CORE:
  POST-ROUNDING / CARRY-PRESERVING DELAYED FUSION

DO_NOT_CLAIM:
  single MultKey;
  packed coefficient envelope;
  Moore/Frobenius map;
  restricted-subspace transform;
  joint correction-map fusion;
  sparse automorphism transform

CANDIDATE_STATUS:
  RETAIN ONLY IF NATIVE VALUE GATE PASSES

PENDING_BASELINE_TIMER:
  UNCHANGED / DO NOT RERUN

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Reopening / kill condition

If the pending baseline timing gate shows insufficient latency headroom, kill this RMFE delayed-fusion branch regardless of the narrow novelty boundary.

If timing passes, the next novelty step should be a citation-forward/citation-backward audit centered on:

- Chen-Han 2018 slim bootstrapping;
- Aung 2025 RMFE bootstrapping;
- Ma 2024 restricted-subring linear transforms;
- Peikert-Pepin 2025 packed bootstrapping,

looking specifically for any post-rounding merge of independently rounded branches against a common encrypted secret/key.

AI_PROVISIONAL_CHOICE:
  RETAIN_NARROW_POSTROUND_DELAYED_FUSION_PENDING_NATIVE_VALUE
  DO_NOT_PROMOTE_TO_PAPER_CLAIM_YET

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
