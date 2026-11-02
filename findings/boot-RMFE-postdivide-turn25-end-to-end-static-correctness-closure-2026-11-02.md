# BOOT Research Turn 25/25 — end-to-end static correctness closure / cross-slot lift-independence audit

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., ePrint 2025/350 / PKC 2025

## Purpose of the final substantive turn

Turn24 repaired a real modulus mismatch:
- production tagged forward is an application-mod5 transform;
- temporary mod625 appears only after recryptEkey reconstruction.

Earlier turns also revised:
- reconstruction exactness/metadata (Turn22);
- pure inverse normalization to scalar-unit28 and Algorithm4 initial factor67 (Turn16);
- factor67 unit closure through Algorithm4 (Turn23);
- final Recode at ptxtSpace5 (Turn20).

The final substantive turn therefore performs a typed end-to-end dependency audit rather than one
more local API audit.

Primary hypothesis:
under the pinned HElib source semantics and Aung's stated RMFE/Algorithm4 theorem assumptions, every
semantic edge in the CURRENT candidate has a compatible domain/codomain, plaintext modulus,
intFactor requirement, and representation invariant. Any remaining blockers should be native
evidence-order blockers, not an unproved static semantic edge.

Falsifier:
find one edge whose output type is not the next edge's input type under the current Turn16-24
supersessions.

No native execution, performance, DFR, or novelty conclusion is claimed.

## Read-before-write duplicate/supersession audit

Current durable GitHub authority before this write:
  HEAD 22d50cad999b90f8163c241b95dc9c390faac645.

GitHub Notes read_repo_file returned empty objects, so existing findings were recovered by direct
GitHub fetch from current HEAD. This is connector degradation, not absence.

Historical library findings were consulted where current GitHub findings intentionally depend on
older theorem results:
- tagged-branch ThinEvalMap special-case theorem;
- full-domain 17-call pruned recovery;
- four-output recombination / branch routing.

Important stale statements identified and excluded:
1. historical candidate paths with one pre-nonlinear shared forward/middle;
2. historical actual-forward-exact-over-Z625 wording;
3. Turn15 current initial intFactor=1;
4. any requirement that reconstructed higher p-adic digits preserve an exact lifted rho relation;
5. historical transform count 19.

Current path has five branch-local forwards and five helper-A preprocesses before aggregation.

## Source facts from Aung needed for the final edge

The public ePrint text gives:
- BGV plaintext CRT is a direct product E^ell and ciphertext addition/multiplication act
  component-wise in the SIMD slots;
- Algorithm4 takes one z in im(phi) in the slot algebra;
- its proof assumes z = sum_t a_t phi(e_t), with each a_t in Z_{p^e};
- the proof concludes correctness for the integers RMFE-packed into that input;
- correction-style CtxtsToSlots computes the digit-extraction ciphertext and correction images using
  constant multiplications and ciphertext additions.

Thus Algorithm4's theorem is slot-local. It does not quantify over or require a relation between
the higher p-adic representatives selected independently in two different SIMD slots.

The mandated web screenshot attempt for the relevant official PDF page failed with a cache-miss
backend error. The official indexed PDF text was readable; no visual-page claim is made.

## 1. New final edge: independent arbitrary lifts across physical SIMD slots are sufficient

After Turn24, the correct reconstruction theorem is residue-only across the mod5-to-mod625 bridge.

For physical slot h, let the five recovered and routed coefficients be:

  a_1^(h),...,a_5^(h) in Z625

with:

  a_i^(h) mod5 = x_i^(h).

There is NO requirement that:
  a_i^(0) and a_i^(1)

be related by a common Hensel lift, rho image, Teichmuller representative, or any other cross-slot
higher-adic relation.

Define independently in each slot:

  z_h = sum_i a_i^(h) phi(e_i).

Then:
  z_h in im(phi)

exactly over Z625 for each h.

Aung Algorithm4 applies to each z_h because its quantified inputs are arbitrary coefficients in
Z_{p^e}. SIMD homomorphic evaluation applies the same circuit component-wise, so each physical slot
satisfies the theorem independently.

Therefore:
  cross-slot higher-adic lift coherence is NOT a correctness precondition.

## 2. Why the existing 443/routing constants remain correct after Turn24

For the first physical slot, after the mod5 tagged-forward / temporary-lift / inverse bridge, a
selected leaf at coordinate j has an arbitrary lift:

  a_tilde in Z625
  a_tilde mod5 = intended branch scalar.

For the second physical slot, the global-tag coordinate transport is only required modulo5.

On every nonzero selected coordinate, the rho unit reduces to:

  182 mod5 = 2.

Thus a raw second-slot selected leaf may be any:

  b_tilde in Z625
  b_tilde mod5 = 2*b

for the branch b determined by the known rho permutation.

The existing public correction uses:

  443 = 182^{-1} mod625.

Although no exact lifted relation b_tilde = 182*b_lift is assumed anymore, 443 is still a valid
unit-lift correction because:

  443 mod5 = 3
  3*2 = 1 mod5.

Define:

  b' = 443*b_tilde mod625.

Then:

  b' mod5 = b.

So b' is simply another arbitrary Z625 lift of the intended branch scalar.

That is exactly sufficient for Algorithm4.

Consequences:
- the existing rho permutation remains valid;
- the existing public factor443 remains valid;
- its correctness rationale is now RESIDUE CORRECTION, not exact reconstruction of a canonical
  182-related lift;
- the historical public-constant norm/cost audit is unchanged because the actual constants are
  unchanged.

At coordinate0 no unit correction is required.

## 3. Four correction outputs remain exact for the actual lifts

After routing/permutation/unit correction, each physical slot h has its own vector:

  A^(h) = (a_1^(h),...,a_5^(h)) in Z625^5

with correct source residues.

For each t=0,1,2,3 define in that slot:

  L_t^(h) = sum_i a_i^(h) phi(e_i)^(5^t).

The candidate public slot-encoded constants realize exactly these expressions component-wise.

Therefore:
- L0^(h)=phi(A^(h)) is exactly in im(phi);
- L1,L2,L3 are exactly the source correction maps for this same chosen arbitrary lift vector
  A^(h);
- no equality of A^(0) and A^(1), and no lifted rho relation between them, is required.

This repairs the current interpretation of Turn15's statement that both physical slots have exact
Algorithm4 inputs:
the statement remains TRUE, but each slot may use a DIFFERENT arbitrary Z625 lift vector.

## 4. Typed end-to-end dependency graph

### E0 — source application ciphertext
Type:
  RMFE-packed application ciphertext
  ptxtSpace=5
  source factor f_in a unit mod5.

Status:
  source baseline contract.

### E1 — SlotsToCtxts
Output:
  five thin branches;
  every physical slot is a scalar x_i,j in Z5;
  common ptxtSpace5;
  common f_in.

Evidence:
  Turns19 and21.

### E2 — global monomial tag
Output:
  same ptxtSpace5 / common f_in;
  branch physical slots become the source-shaped tagged extension states.

Evidence:
  Turn19 plus historical tagged-branch theorem.
  Monomial tag has unit canonical norm.

### E3 — five branch-local forward ThinEvalMap calls
Output:
  five coefficient-domain states modulo5.

Exact theorem:
  Tagged ThinForward5 = desired FullForward5 on the special source-shaped tagged branch.

Evidence:
  Turn24 superseding the older Z625-forward wording.

### E4 — five branch-local stock preprocessing helper-A paths
Operations:
  source level preparation;
  canonicalization/modDown;
  reLinearize(recryptKeyID);
  rawModSwitch(q=626);
  branch-local source checks;
  newMakeDivisible(5);
  exact integer /5.

Output:
  five exact arbitrary-precision ZZX pairs.

No thin-slot invariant after E3.

Evidence:
  Turn18 and historical tagged theorem.

### E5 — exact pair aggregation + one shared reconstruction
Output:
  ptxtSpace625 ciphertext R_shared;
  intFactor1;
  keyID0;
  same primeSet as recryptEkey.

Exact identity:
  R_shared = sum_i R_i at ciphertext-parts level.

Residue:
  red5(R_shared plaintext)
    = sum_i tagged forward5 states.

Evidence:
  Turns22 and24.

### E6 — pure normal_basis=false Z625 inverse
Output:
  arbitrary full-ring U625.

Reduction theorem:
  red5(B625(U)) = B5(red5(U)).

Hence selected coordinates reduce to the intended tagged branch residues.

Resource contract:
  stock order2 outer + FULL Frobenius key object is sufficient.

Evidence:
  Turns16,17,24.

### E7 — scalar-unit28 + full-domain target-pruned recovery
Operations:
  multByConstant(28L);
  17 Frobenius calls / 13 distinct exponents;
  full-domain even/odd split identities;
  exact current routing.

Output:
  five selected scalar ciphertext leaves in Z625.

They are arbitrary lifts with correct residues.

Common factor after scalar-unit28:
  67.

Evidence:
  Turn16 plus historical full-domain/pruned recovery theorem and frozen canary source.

### E8 — slotwise routing / rho residue correction
Output:
  for EACH physical slot independently, five arbitrary Z625 branch lifts in the source branch order.

Nonzero second-slot residue correction:
  multiply by public unit443.

No cross-slot lift coherence required.

Evidence:
  NEW Turn25 theorem.

### E9 — four correction recombinations
Output in each physical slot:
  L0,L1,L2,L3 built from the SAME local arbitrary-lift vector.

Exact:
  L0 in im(phi);
  Lt = sum_i a_i phi(e_i)^(5^t).

Evidence:
  historical four-output recombination audit, refined by Turn25.

### E10 — Algorithm4
Input:
  arbitrary Z625 lifts;
  eta=125=p^(e-1);
  common initial factor67, a 5-adic unit.

Operations:
  six divideByP boundaries:
    625->125
    625->125
    125->25
    625->125
    125->25
    25->5.

Correctness:
  Aung divisibility theorem applies independently per SIMD slot;
  pinned HElib factor harmonization preserves semantics;
  divideByP realizes semantic quotient;
  all dynamic factors remain 5-adic units.

Evidence:
  Turns15 and23, with Turn16/23 superseding Turn15's old initial-factor1 statement.

### E11 — final Recode
Input/output:
  ptxtSpace5.

Map:
  mod5 reduction of pi=phi o psi.

Existing 625-typed evaluation-key family remains compatible through gcd(5,625)=5.

Evidence:
  Turn20.

### E12 — restore source application factor
Operation:
  final.multByConstant(InvMod(f_in,5)).

Effect:
  public scalar-unit metadata path restores factor f_in with no direct part/noise multiplication.

Placement:
  only after final Recode.

Evidence:
  Turns18 and20.

## 5. End-to-end static theorem

Under the following explicit assumptions:
A1. The pinned HElib ordinary branch-local recryption correctness preconditions/source bounds hold
    for each branch.
A2. The source Aung SlotsToCtxts and Algorithm4 RMFE contracts hold for the selected parameters.
A3. The current fixed parameter/key contracts are:
    p=5,m=32768,k=5,r=1,e=4,ePrime=1,q=626,
    temporary ptxtSpace625,
    J=[0,1024,7168,2048,6144],
    branch labelling [2,0,3,1,4].
A4. Native implementation follows the current Turn18 source-refactor cut:
    five helper-A executions, exact pair sum, one helper-B reconstruction.
A5. No stale pre-aggregation/shared-forward architecture is substituted.

Then the CURRENT candidate has a coherent static semantic path:

  source RMFE application plaintext
  -> five scalar Z5 branches
  -> tagged mod5 coefficient states
  -> one arbitrary Z625 lift of their aggregate
  -> five independently valid arbitrary Z625 branch lifts
  -> slotwise exact L0..L3
  -> Algorithm4 digit extraction
  -> final mod5 Recode
  -> source-factor restoration,

and returns the same application plaintext tuple modulo5.

There is no remaining identified STATIC semantic edge requiring a new theorem for this fixed
candidate.

This is a conditional STATIC/MATH closure, NOT complete candidate correctness.

## 6. Supersessions frozen by this audit

The following statements MUST NOT appear in the current paper/prototype specification:

1. actual tagged forward is exact over Z625.
   Replace with:
     exact over Z5 + arbitrary Z625 lift bridge.

2. Algorithm4 initial factor is1.
   Replace with:
     common factor67 before Algorithm4; dynamic factors remain 5-adic units.

3. reconstructed second physical slot is exactly the first-slot lift under rho/182.
   Replace with:
     only mod5 rho residue/permutation is required; public443 maps it to an arbitrary correct lift.

4. candidate uses one shared forward or one full preprocessing helper.
   Replace with:
     five branch-local forward/helper-A paths;
     aggregate only exact post-divide pairs;
     one helper-B reconstruction.

5. transform-side count19.
   Current structural count is:
     five forward transforms
     + one pure inverse outer stage
     + seventeen recovery Frobenius calls
     = 23 transform-side calls/stages under the established ledger.
   This remains NOT a latency claim.

6. generic ThinEvalMap correctness on arbitrary extension-valued input.
   Still false.

## 7. What remains genuinely unproven

Static semantic theorem edges:
  no currently identified gap for the fixed construction.

But evidence order remains incomplete:

2. small correctness canary:
   revised recovery-only canary NOT EXECUTED;

3. exact parameter/interface:
   NOT EXECUTED;

4. complete source-faithful Aung baseline correctness:
   PENDING;

5. complete candidate native correctness:
   PENDING;

6. noise/security/DFR:
   PENDING;

7. matched benchmark:
   BLOCKED by correctness;

8. independent raw audit:
   PENDING.

Exact Aung artifact runtime state remains unverified where previously recorded.

Therefore:
  STATIC_THEOREM_CLOSURE != CORRECTNESS_GATE_PASS.

## Verdict

PASS_CROSS_SLOT_ARBITRARY_LIFT_INDEPENDENCE
PASS_RHO_RESIDUE_CORRECTION_WITH_PUBLIC_443
PASS_SLOTWISE_FOUR_CORRECTION_HANDOFF
PASS_CURRENT_END_TO_END_STATIC_TYPED_CORRECTNESS_CLOSURE
PASS_NO_IDENTIFIED_STATIC_SEMANTIC_EDGE_GAP

SUPERSEDE_EXACT_LIFTED_RHO_COHERENCE_REQUIREMENT
SUPERSEDE_STALE_TRANSFORM_COUNT_19_WITH_23

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

The candidate remains ACTIVE.

## Next decisive test after session handoff

No further substantive turn should be spent on static source microaudits unless a native result
falsifies one of the frozen interfaces.

The next evidence-order action is:
execute the frozen revised recovery-only HElib canary at
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After its PASS:
run the current exact parameter/interface oracle, including:
- SlotsToCtxts scalar/common-factor assertions;
- ptxtSpace5 tagged-forward oracle;
- shared-vs-separate reconstruction state equality;
- mod5-to-Z625 lift bridge;
- real normal_basis=false inverse;
- factor1 -> scalar28 -> factor67;
- exact recovery/routing/L0..L3;
- independent per-slot arbitrary-lift correction;
- six Algorithm4 divide boundaries/unit-factor instrumentation;
- final Recode at ptxtSpace5;
- f_in restoration.

Do not time the candidate before these correctness checks pass.
