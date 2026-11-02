# BOOT Research Turn 21/25 — SlotsToCtxts scalar-slot domain closure gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., ePrint 2025/350 / PKC 2025

## Primary hypothesis

Historical Turn 23 proves the tagged-branch ThinEvalMap theorem only for branches whose physical
SIMD slots are base-ring scalars before the global monomial tag.

Turn 21 asks whether this precondition is actually guaranteed by Aung's source SlotsToCtxts
interface, rather than being an extra assumption silently imposed by the candidate.

Hypothesis:
for both Aung SlotsToCtxts methods used in the two correction workflows, every output branch is
thinly packed in the literal source sense: each physical SIMD slot contains one integer
x_{i,j} in Z_p, hence a constant element of the HElib slot algebra. Therefore the five current
p=5 branches lie exactly in the pre-tag scalar domain required by Turn 23.

Falsifier:
- Aung's SlotsToCtxts outputs are only projection ciphertexts in a sub-Galois ring G but may remain
  nonconstant extension elements;
- Method 2 returns recoded extension elements rather than the integers x_{i,j};
- "thinly packed" is only informal and not tied to slot values in Z_p;
- or pinned HElib ThinEvalMap's domain notion of constant does not match the Z_p subring used by
  Aung.

No native execution, artifact-byte authentication, or timing is claimed.

## Closest prior mechanism / exact source contract

Aung Algorithm 2 begins with:

  c1,...,ck <- SlotsToCtxts(c)

and then applies MultKey independently to each ci.

Section 5.1 gives the full semantic contract.

Let:
  {x_{1,0},...,x_{k,0},...,x_{1,l},...,x_{k,l}}

be the message encrypted in the RMFE-packed ciphertext.

The source explicitly assumes:

  all x_{i,j} are integers lying in Z_p.

Then it states:

  SlotsToCtxts splits a single RMFE-packed ciphertext into k-many thinly-packed ciphertexts.

More precisely, for every 1 <= i <= k, the i-th thin ciphertext encrypts:

  {x_{i,0},...,x_{i,l}}.

Thus the source specification directly identifies the plaintext in each output physical SIMD slot.

The official ePrint PDF text was readable. Developer-mandated screenshot attempts for the relevant
PDF pages were made and failed with HTTP 403 from the screenshot backend; no visual-page claim is
made beyond the indexed official PDF text.

## 1. Method 1 output is an integer scalar in every physical slot

Aung Method 1 applies projection maps:

  tau_1,...,tau_k.

Earlier in Section 4.3 these are defined so that if an RMFE-packed element alpha decodes as:

  psi(alpha) = (a_1,...,a_k),

then:

  tau_i(alpha) = a_i.

At the SlotsToCtxts interface, the source message coordinates satisfy:

  a_i = x_{i,j} in Z_p.

Therefore for physical SIMD slot j:

  slot_j(c_i) = tau_i(slot_j(c)) = x_{i,j} in Z_p.

Although tau_i is formally a map into the sub-Galois ring G, the actual source-restricted image on
these application messages is the embedded base ring Z_p subset G.

Hence no residual extension coordinate remains in a Method-1 output branch.

## 2. Method 2 output is also an integer scalar

Method 2 first applies the recode map so that physical SIMD slot j holds:

  sum_i x_{i,j} phi(e_i) in im(phi).

It then applies projection maps tau'_i satisfying:

  tau'_i(sum_h x_{h,j} phi(e_h)) = x_{i,j}.

Again:

  x_{i,j} in Z_p.

Therefore the final SlotsToCtxts branch after Method 2 has:

  slot_j(c_i) = x_{i,j} in Z_p.

The intermediate recoded ciphertext is extension-valued, but the candidate does not tag or thin-
bootstrap that intermediate object. The candidate starts only from the final SlotsToCtxts outputs.

Thus Method 2 also satisfies the scalar precondition.

## 3. This is exactly HElib's thin-slot domain

Pinned include/helib/EvalMap.h documents ThinEvalMap as the linear transform for:

  "thin" bootstrapping, where slots are assumed to contain constants.

For BGV at application plaintext space p=5,r=1, the physical slot algebra is an extension E of:

  Z_p = Z_5.

An element x_{i,j} in Z_5 embeds as the degree-zero constant polynomial in E.

Therefore Aung's literal SlotsToCtxts output type:

  x_{i,j} in Z_5

is exactly the HElib constant-slot domain expected before a thin transform.

No interpretation bridge or extra scalarization operation is needed.

## 4. Physical-slot statement, not only logical RMFE statement

This closure is stronger than saying merely that the RMFE vector components are integers.

Aung Section 5.1 states that the i-th output CIPHERTEXT encrypts the sequence:

  {x_{i,0},...,x_{i,l}}.

Since j indexes the ordinary SIMD slots, this is a direct physical-slot specification:

  physical slot j of c_i contains x_{i,j}.

Thus for current m=32768 with two HElib physical SIMD slots, each of the five branches has the form:

  (a_i,b_i) in Z_5^2

before candidate tagging.

This is precisely the starting point used by historical Turn 23.

## 5. Exact connection to the tagged-branch theorem

Historical Turn 23 established:

starting from a scalar physical pair:

  (a,b) in S^2,

global monomial tagging by X^J gives:

  (a X^J, b rho(X^J)),

and stock forward ThinEvalMap on this special tagged state equals the desired full forward action
exactly.

Turn 21 now closes the missing source precondition:

  Aung SlotsToCtxts
    -> (a_i,b_i) in Z_5^2
    -> global tag
    -> Turn-23 exact tagged ThinEvalMap theorem.

The generic statement:

  ThinEvalMap is valid on arbitrary extension-valued slots

remains FALSE and is not revived.

The only valid production path is the source-shaped scalar branch followed by the audited global
monomial tag.

## 6. Compatibility with Turn 19 common-factor result

Turn 19 proved source-faithful SlotsToCtxts linear execution preserves the common representation:

  ptxtSpace = 5,
  intFactor = f_in.

Turn 21 adds the independent semantic slot-type statement:

  every physical slot value lies in Z_5.

Together, immediately before tagging, every branch satisfies:

  context/pubKey: common
  ptxtSpace: 5
  intFactor: common f_in
  physical slot values: base-ring scalars in Z_5.

This is now the complete pre-tag type contract.

## 7. No new conversion / recode is needed before tagging

Because SlotsToCtxts already returns thinly-packed integer branches, the candidate must NOT insert:
- another RMFE decode;
- another Recode;
- a trace-to-base-field operation;
- a local coefficient extraction;
- or a scalarization transform

before applying the global monomial tags.

Any such extra conversion would be non-source work and would alter the cost/noise comparator.

The canonical branch input to tagging is simply the source SlotsToCtxts output.

## 8. Primary Corr./TnM consequence

The primary candidate comparator is Corr./TnM.

Aung Section 6.1 specifies that Corr./TnM uses Method 1 for SlotsToCtxts.

Therefore the primary baseline enjoys the strongest direct form of this contract:

  each branch is directly tau_i(input),
  and each physical slot is x_{i,j} in Z_p.

No Method-2 intermediate recode is involved in the primary comparator.

## 9. Native correctness assertions

The first full native parameter/interface gate should assert this source contract immediately after
SlotsToCtxts and BEFORE tagging.

For deterministic plaintext patterns, use a correctness-only secret-key harness to decode both
physical SIMD slots of every branch and require:

  slot_j(c_i) == expected x_{i,j} mod 5

for:
  i = 0,...,4,
  both physical slots j.

Additionally assert that each decoded slot polynomial has degree zero / equals the base-ring
constant representation.

Then, after global tag X^J_i, verify the exact Turn-23 tagged representation:

  first physical slot = x_{i,0} X^J_i
  second physical slot = x_{i,1} rho(X^J_i).

Any nonconstant pre-tag branch output is:

  FAIL_SLOTS_TO_CTXT_SCALAR_DOMAIN

and invalidates candidate timing.

## 10. Evidence boundary

Established:
- source functional specification of both SlotsToCtxts methods outputs thinly-packed ciphertexts;
- every output physical slot is exactly an x_{i,j} in Z_p;
- pinned HElib ThinEvalMap calls this exact base-ring situation its constant/thin domain;
- Turn-23 tagged-scalar theorem therefore applies to the source outputs.

Not established:
- exact Aung implementation bytes;
- runtime decoded branch values;
- native ciphertext correctness;
- DFR/capacity/performance.

AUNG_ARTIFACT_RUNTIME_SCALAR_SLOT_STATE remains UNVERIFIED.

## Verdict

PASS_SLOTS_TO_CTXT_SOURCE_SCALAR_SLOT_DOMAIN
PASS_METHOD1_PHYSICAL_ZP_OUTPUTS
PASS_METHOD2_FINAL_PHYSICAL_ZP_OUTPUTS
PASS_HELIB_THIN_DOMAIN_MATCH
PASS_TURN23_PRECONDITION_SOURCE_CLOSURE

AUNG_ARTIFACT_RUNTIME_SCALAR_SLOT_STATE=UNVERIFIED
NATIVE_EXECUTION=NOT_OBTAINED

This closes the source-level scalar-slot precondition behind the candidate's tagged ThinEvalMap path.

CORRECTNESS_GATE remains BLOCKED because the evidence-order recovery canary and all subsequent
native correctness gates remain absent.

BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

The evidence-order blocker remains the revised recovery-only canary.

After that PASS, the Turn-18/19 exact parameter-interface gate must include the Turn-21 source-domain
assertions:
1. SlotsToCtxts outputs exact expected Z_5 scalars in every physical slot;
2. each pre-tag slot is degree-zero in the HElib slot algebra;
3. common ptxtSpace=5 and common f_in;
4. global tag produces the exact Turn-23 two-slot tagged representation;
5. only then call stock branch-local thin forward and helper A.

No timing or capacity interpretation is authorized before these assertions pass.
