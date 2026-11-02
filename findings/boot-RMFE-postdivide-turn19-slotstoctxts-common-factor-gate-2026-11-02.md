# BOOT Research Turn 19/25 — SlotsToCtxts common-ptxtSpace / common-intFactor gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., ePrint 2025/350 / PKC 2025

## Research-turn selection

A first candidate question for this turn was tagged-branch ThinEvalMap typing.
Read-before-write recovery found this was already durably closed by historical BOOT Turn 23
and summarized again in the Turn-24 milestone. It would therefore be a low-information duplicate
and was not used as the Turn-19 primary scientific step.

## Primary hypothesis

Turn 18 assumes the five outputs of Aung SlotsToCtxts have a single common source application
plaintext space and a single common BGV intFactor f_in.

Hypothesis:
for both source SlotsToCtxts methods, a source-faithful realization using pinned HElib standard
linear-map machinery preserves the input ciphertext application ptxtSpace and intFactor in every
split branch. Thus all five current k=5 branches enter tagging / thin forward with the SAME
ptxtSpace=5 and SAME f_in.

Falsifier:
- a source SlotsToCtxts method requires ciphertext-ciphertext multiplication;
- standard HElib linear-map execution changes intFactor branch-dependently;
- some branch changes plaintext space before the candidate middle;
- or Method 2 recode/projection introduces a nonlinear or factor-changing operation.

This turn does not claim exact public artifact bytes or native execution.

## Source provenance / closest mechanism

Aung Algorithm 2 first computes c1,...,ck = SlotsToCtxts(c), then executes MultKey independently.

Section 5.1 defines:
Method 1: evaluate projection maps tau_1,...,tau_k.
Method 2: apply the recode map, then evaluate projection maps tau'_1,...,tau'_k.

The paper's cost descriptions for these maps use only automorphisms, additions, and
constant-ciphertext multiplications. No ciphertext-ciphertext multiplication is part of
SlotsToCtxts.

Section 6.1 assigns Method 1 to correction trace-and-merge and Method 2 to correction BSGS.

The mandated screenshot attempt on the official ePrint PDF failed with HTTP 403 in the screenshot
backend; official PDF text extraction remained available. This limitation is recorded.

## 1. Input plaintext space

Current application parameters are p=5, r=1, so P_app=5.

SlotsToCtxts occurs before the recryption middle raises the temporary bootstrap algebra to 625.
Thus its common input ptxtSpace is 5.

## 2. Pinned HElib linear-map primitive inventory

Standard HElib MatMul / linear-map execution uses:
- automorphisms / smartAutomorph;
- relinearization under the same logical key ID;
- encoded PUBLIC polynomial constants through zzX/ZZX/DoubleCRT;
- ciphertext additions;
- cleanup / ordinary modulus switching as needed.

There is no ciphertext-ciphertext multiplication in the linear-map executor.

## 3. Automorphisms preserve ptxtSpace and intFactor

Pinned Ctxt::automorph changes ring coordinates / SKHandle powerOfX and does not modify ptxtSpace or
intFactor. smartAutomorph relinearizes without plaintext multiplication.

MatMul automorphism precomputation also copies the input intFactor into its result ciphertext.

Hence every automorphic image retains:
  ptxtSpace = 5
  intFactor = f_in.

## 4. Public polynomial constants preserve intFactor

MatMul ConstMultiplier uses Ctxt::multByConstant with zzX/ZZX or DoubleCRT. These encoded-public
polynomial overloads multiply ciphertext parts and update noise bounds but do not modify BGV
intFactor.

They must be distinguished from the special scalar long/ZZ overload that can represent a
plaintext-unit multiplication by changing intFactor. Standard MatMul diagonal execution does not
use that scalar metadata shortcut.

The raw polynomial/DoubleCRT paths also leave ptxtSpace unchanged.

## 5. Same-factor additions preserve the common factor

All terms in one source linear map originate from the same input and retain f_in.
Pinned Ctxt::addCtxt only performs BGV factor harmonization when incoming intFactors differ.
Here they do not.

Therefore no harmonization factor is selected and every output projection retains f_in.

## 6. Cleanup / real modulus switching does not split factor state

Pinned MatMul may perform cleanup around automorphisms. The active BGV modDownToSet branch performs
real modulus switching and does not modify intFactor. The degenerate-drop branch that would alter
intFactor is disabled by its literal false guard.

Different output branches may still have different noiseBound or prime-set histories. Turn 18 does
not require those to be equal before its own source-normalized branch preparation.

## 7. Method 1 invariant

Aung Method 1 consists of k public linear projection maps tau_i.
Starting from one ciphertext with state (5,f_in), each output therefore has exactly:
  ptxtSpace = 5
  intFactor = f_in.

For current k=5 all five branches share f_in.

## 8. Method 2 invariant

Aung Method 2 composes a public linear recode map with public linear projections tau'_i.
Each pinned source-faithful linear map preserves the same representation invariant:
  input (5,f_in)
  -> recode (5,f_in)
  -> every projection output (5,f_in).

The extra recode changes cost but not this factor invariant.

## 9. Primary Corr./TnM consequence

Aung Section 6.1 assigns correction trace-and-merge to SlotsToCtxts Method 1.
Therefore the primary selected baseline has a direct source-level contract:
  all five SlotsToCtxts outputs have ptxtSpace=5 and intFactor=f_in.

This is exactly the precondition used by Turn 18's candidate-facing PubKey middle.

## 10. Global tagging preserves the invariant

The current candidate then multiplies branch i by the global monomial X^J_i using the polynomial
ZZX constant path. That path does not modify intFactor or ptxtSpace.

Thus immediately before Turn-18 pre-forward preparation all five tagged branches still share:
  ptxtSpace = 5
  intFactor = f_in.

Historical Turn 23 already proves semantic correctness of tagged stock forward ThinEvalMap and is
not re-proved here.

## 11. What remains unverified

The paper defines the source linear-map methods, but no exact public Aung implementation artifact was
authenticated here.

Therefore:
  SOURCE-FAITHFUL SLOTS-TO-CTXS COMMON FACTOR: PASS
  AUNG ARTIFACT ACTUAL RUNTIME intFactor equality: UNVERIFIED.

Future matched code must assert this invariant.

Required native assertions immediately after SlotsToCtxts and after tagging:
  branch ptxtSpace == 5
  branch keyID == common key ID
  internal/debug intFactor == f_in for all five branches.

Because intFactor has no public getter, the factor assertion belongs inside Turn-18 PubKey/friend
instrumentation or a HELIB_DEBUG-only helper.

## 12. Construction consequence

Turn 18's one-factor handoff requires no redesign.
The candidate-facing PubKey method can read f_in from one branch, assert the other four match,
proceed with five branch-local preprocesses, and return the single f_in for final mod-5 restoration.

No per-branch factor normalization and no extra representation-noise step is needed under the
source-faithful construction.

## Verdict

PASS_SLOTS_TO_CTXT_COMMON_PTXTSPACE
PASS_SOURCE_FAITHFUL_COMMON_INTFACTOR
PASS_CORR_TNM_METHOD1_COMMON_FACTOR
PASS_CORR_BSGS_METHOD2_COMMON_FACTOR
PASS_TAGGING_PRESERVES_COMMON_FACTOR
AUNG_ARTIFACT_RUNTIME_FACTOR_STATE=UNVERIFIED

NATIVE_EXECUTION=NOT_OBTAINED

CORRECTNESS_GATE remains BLOCKED.
BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

The evidence-order blocker remains the revised recovery-only canary.

After that PASS, the Turn-18 exact parameter/interface test must assert:
- after SlotsToCtxts, all five branches have ptxtSpace=5 and common f_in;
- after global tagging, the invariant is unchanged;
- only then enter branch-local stock pre-forward preparation and helper A.

If an actual matched Aung artifact produces differing branch factors, stop and localize the
nonstandard scalar/metadata operation before any candidate timing.
