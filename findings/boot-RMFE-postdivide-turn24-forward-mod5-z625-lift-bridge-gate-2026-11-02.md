# BOOT Research Turn 24/25 — tagged-forward mod-5 to Z625-lift bridge gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Research-turn selection / duplicate avoidance

The initially proposed Turn-24 question was whether any hidden thin-slot assumption remains after
the globally tagged forward ThinEvalMap.

Read-before-write found this was already durably closed in historical:

  boot-r23-tagged-branch-thinevalmap-typing-gate.md

whose Section 6 explicitly proves that after slotToCoeff the recryption middle uses only generic
ciphertext/ring operations and has no further thin-slot assumption.

A second candidate question—whether tag noise invalidates branch-local recryption bounds—was also
already closed in historical:

  boot-r19-late-aggregation-noise-capacity-gate.md

which proves the monomial tag has canonical norm1 and source recryption checks remain branch-local.

Neither duplicate was counted as Turn24's scientific step.

The dependency audit instead exposed a previously unstated modulus boundary:
historical tagged-forward statements were phrased over Z625, whereas the actual source forward
ThinEvalMap is constructed from context.getEA() and therefore operates at application r=1,
plaintext space5. The temporary Z625 algebra appears only after recryptEkey reconstruction.

This turn closes that exact bridge.

## Primary hypothesis

For the current p=5,r=1,e=4,ePrime=1 thin-bootstrap path:

1. the tagged source branch is transformed by ThinEvalMap over the application ring modulo5;
2. the branch-local recryption middle/reconstruction lifts that mod5 coefficient state to an
   arbitrary plaintext in the temporary ring modulo625;
3. the candidate applies a full normal_basis=false inverse EvalMap over Z625.

Hypothesis:
although the forward tagged theorem is only required and actually instantiated modulo5, the
temporary Z625 inverse/recovery path still returns selected branch coefficients whose residues
modulo5 are exactly the source branch messages. Therefore arbitrary higher 5-adic digits are harmless
and Aung Algorithm4's arbitrary-lift theorem applies.

Falsifier:
- the actual slotToCoeff is built over the temporary 625 algebra;
- the mod5 ThinEvalMap tagged identity does not match reduction of the full forward map;
- the temporary full inverse over625 does not reduce modulo5 to the inverse of the mod5 full
  forward map;
- or later correctness needs equality of the selected coefficients over all of Z625 rather than
  only correct residues modulo5.

No native execution or performance claim is made.

## 1. Source: forward and inverse live at different plaintext exponents

Pinned ThinRecryptData::init first calls RecryptData::init.

RecryptData::init records application:

  r = context.getAlMod().getR() = 1.

It creates the temporary recryption algebra:

  alMod = PAlgebraMod(context.getZMStar(), e-ePrime+r)
        = PAlgebraMod(...,4),

and:

  ea = EncryptedArray(context,*alMod),

so the temporary plaintext space is:

  5^4 = 625.

ThinRecryptData::init then constructs:

  coeffToSlot = ThinEvalMap(*ea,...,invert=true,...)

using the temporary r=4 algebra, BUT constructs:

  slotToCoeff = ThinEvalMap(context.getEA(),...,invert=false,...)

using the ordinary application EncryptedArray.

Therefore the production forward boundary is exactly:

  ptxtSpace 5 / r=1,

not 625.

This source fact supersedes any statement that the actual branch-forward ciphertext is transformed
as a Z625 plaintext.

## 2. Exact corrected tagged-forward theorem is modulo5

Historical tagged-branch algebra used the lifted matrix:

  A625 = [[1,1],[443,182]].

Reducing coefficients modulo5 gives:

  A5 = [[1,1],[3,2]].

The historical global-monomial rho relations reduce likewise:

  rho5(X^0)    = X^0
  rho5(X^1024) = 2 X^7168
  rho5(X^7168) = 2 X^1024
  rho5(X^2048) = 2 X^6144
  rho5(X^6144) = 2 X^2048.

For source scalar physical slots:

  (a,b) in Z5^2,

global tag X^j gives the actual pair:

  (a X^j, b rho5(X^j)).

Pinned forward ThinEvalMap at r=1 applies A5 to those physical values.

Because b is a base-ring scalar:

  rho5(b X^j) = b rho5(X^j).

Thus:

  ThinForward5(Tag_j(a,b))
    = FullForward5(a X^j,b X^j)

exactly over the application ring modulo5.

This is the production theorem.

The stronger wording:

  actual forward is exact over Z625

is unnecessary and should no longer be used.

## 3. Consistency check with the lifted inverse matrix

The historical lifted one-factor full-forward matrix has:

  A625 = [[1,1],[443,182]]

and inverse:

  A625^{-1} = [[313,91],[313,534]].

Coefficient reduction modulo5 gives:

  A625 mod5 = [[1,1],[3,2]]

and:

  A625^{-1} mod5 = [[3,1],[3,4]].

Direct inversion of A5 over Z5 gives:

  A5^{-1} = [[3,1],[3,4]].

Therefore:

  red5(A625^{-1}) = (red5 A625)^{-1}.

This concrete current-instance calculation already verifies the needed inverse/reduction
compatibility for the outer two-slot matrix.

## 4. General source reason the full inverse commutes with reduction

Pinned EvalMap matrix construction is parameterized by the EncryptedArray's PAlgebraMod exponent r.

The temporary inverse uses r=4 and ppInvert(...,p=5,r=4).

Its matrix A625 is invertible over Z/625Z.

Reduction modulo5 is a ring homomorphism. From:

  A625 * A625^{-1} = I mod625,

reduce coefficients modulo5:

  A5 * red5(A625^{-1}) = I mod5.

Hence:

  red5(A625^{-1}) = A5^{-1}.

The same argument applies to every invertible block in the full normal_basis=false EvalMap
factorization, not only the displayed outer 2x2 block.

Therefore the candidate's temporary Z625 pure inverse B625 satisfies:

  red5 o B625 = B5 o red5,

where B5 is the inverse of the corresponding full forward map modulo5.

## 5. What ordinary recryption correctness supplies

Let M5 be the common-coordinate tagged plaintext in the application coefficient/slot algebra
modulo5.

After branch tagged ThinEvalMap:

  C5 = FullForward5(M5).

The branch-local:
  reLinearize
  -> rawModSwitch
  -> newMakeDivisible
  -> /5
  -> recryptEkey reconstruction

does not promise a canonical lift of C5.

Ordinary HElib recryption correctness supplies exactly what is needed:
the reconstructed temporary plaintext T625 satisfies

  red5(T625) = C5.

Equivalently there exists an arbitrary temporary-ring disturbance E625 such that:

  T625 = lift(C5) + 5 E625.

The higher 5-adic digits may occupy the full extension ring.

No sparse/rank-5/Teichmuller lift invariant is required.

## 6. Pure inverse recovers the tagged branch coordinates modulo5

Apply candidate pure inverse B625:

  U625 = B625(T625).

Reduce modulo5:

  red5(U625)
    = B5(red5(T625))
    = B5(C5)
    = B5(FullForward5(M5))
    = M5.

Therefore:

  U625 = lift(M5) + 5 E'625

for some arbitrary full-ring E'625.

In particular, for every selected coordinate j in J:

  coeff_j(U625) mod5
    = intended tagged branch coefficient mod5.

All nonselected coordinates and all higher 5-adic digits remain unrestricted.

This is exactly the input type accepted by the existing full-domain 17-call pruned-unpack theorem.

## 7. Scalar-unit28 normalization does not alter the bridge

The binary split tree returns each target coefficient multiplied by:

  d = 8192 mod625 = 67.

Turn16 normalizes BEFORE the tree using semantic multiplication by:

  28 = 8192^{-1} mod625.

Since 28 is a unit, this changes the temporary semantic plaintext exactly and preserves the
mod5 relation.

Modulo5:

  8192 mod5 = 2
  28 mod5 = 3
  2*3 = 1 mod5.

Therefore normalization is compatible with both:
- full Z625 coefficient extraction;
- the only required source-message residue invariant modulo5.

## 8. Why arbitrary selected Z625 lifts are sufficient downstream

After the pure inverse and pruned tree, each selected leaf is some:

  a_i in Z625

such that:

  a_i mod5 = source branch message.

The candidate does NOT require a_i to equal:
- the canonical integer 0..4;
- a Teichmuller lift;
- the stock branchwise reconstructed lift;
- or any predetermined higher-adic representative.

The four correction ciphertexts are formed exactly as:

  L_t = sum_i a_i * phi(e_i)^(5^t),  t=0,1,2,3.

Hence L0 is exactly in im(phi) over Z625 for these actual a_i.

Turn15 established that Aung Algorithm4 quantifies over arbitrary:

  a_i in Z_{p^e}=Z625,

and its divisibility theorem uses only their p-adic properties.

Thus correct mod5 recovery plus arbitrary Z625 lifting is sufficient for the complete downstream
semantic theorem.

## 9. Consequence for second-slot/rho claims

At the pre-forward boundary, rho compensation is an exact mod5 statement because the ciphertext
plaintext space is5.

After reconstruction, higher 5-adic digits in either physical slot may be dirty and need not obey a
canonical lifted rho relation.

The candidate does NOT require such a relation.

The full Z625 inverse plus full-domain pruned recovery extracts the actual selected scalar lifts in
each physical slot, and the already-audited coordinate routing/RMFE public constants handle the
slotwise outputs. Algorithm4 accepts arbitrary lifts slotwise.

Therefore no claim should be made that the reconstructed higher 5-adic digits preserve the original
tagged rho relation exactly over625.

Only the source residues modulo5 are required.

## 10. Revised canonical theorem statement

The correct end-to-end static bridge is:

  source scalar SlotsToCtxts branches over Z5
  -> global monomial tags over Z5
  -> special-case tagged ThinEvalMap exact over Z5
  -> five independent generic HElib recryption preprocesses
  -> post-divide exact aggregation
  -> one reconstructed arbitrary Z625 lift T625
       with T625 mod5 equal to the tagged forward state
  -> pure normal_basis=false Z625 inverse
       whose reduction is the inverse full map mod5
  -> selected coordinates are arbitrary Z625 lifts of the five source residues
  -> scalar-unit28 normalization / 17-call full-domain recovery
  -> exact L0..L3 on those actual lifts
  -> Aung Algorithm4 arbitrary-lift correctness
  -> final mod5 Recode
  -> restore source f_in.

This replaces any shorthand that treats the application forward as a Z625 transform.

## 11. Native assertions refined by this turn

After the recovery-only canary passes, the exact parameter/interface gate should distinguish two
different oracles.

At application forward:
- assert ptxtSpace == 5;
- compare tagged ThinEvalMap output ONLY modulo5 against FullForward5;
- do NOT assert a nonexistent 625 plaintext equality.

After shared reconstruction:
- assert ptxtSpace == 625;
- decrypt T625 and reduce modulo5;
- require equality to the earlier FullForward5 tagged state.

After pure inverse:
- decrypt U625;
- reduce every selected coordinate modulo5;
- require the five intended branch residues.

Then run the exact Z625 recovery/L0..L3 oracle on the actual lifted U625 state.

Any failure of the reduction bridge is:

  FAIL_FORWARD_MOD5_TO_Z625_LIFT_BRIDGE.

## Verdict

PASS_ACTUAL_FORWARD_PTXTSPACE5_TYPING
REFINE_TAGGED_FORWARD_THEOREM_TO_EXACT_MOD5
PASS_FULL_INVERSE_REDUCTION_COMPATIBILITY
PASS_RECRYPT_Z625_ARBITRARY_LIFT_BRIDGE
PASS_SELECTED_LIFT_RESIDUE_CORRECTNESS
PASS_ALGORITHM4_ARBITRARY_LIFT_HANDOFF

SUPERSEDE_ACTUAL_FORWARD_EXACT_OVER_Z625_WORDING

NATIVE_EXECUTION=NOT_OBTAINED

This closes a genuine modulus/interface gap in the static correctness chain and weakens an older
overstrong statement without weakening the candidate construction.

CORRECTNESS_GATE remains BLOCKED solely because native canary/interface/baseline/candidate evidence
is still absent; this result does not authorize a native PASS claim.

BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
AUDIT_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Primary evidence-order blocker remains the frozen revised recovery-only canary.

After that PASS, exact interface verification must use the two-modulus oracle above:
forward correctness at ptxtSpace5, then reconstruction-lift consistency into ptxtSpace625, then
selected-coordinate residue correctness after the real normal_basis=false inverse.

No timing, capacity, DFR or performance claim is authorized before those native checks pass.
