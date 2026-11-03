# BOOT / B158 — Successor Research Turn 7 — dirty-lift supersession, direct E8 coefficient MultKey, and exact fused-recode envelope

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CONSTRUCTIVE_DESIGN
Native execution: NONE

## Read-before-write / durable authority

Current durable predecessor:
  findings/boot-successor-turn6-e8-subring-lifted-linear-interface-gate-2026-11-03.md
  blob d110ecf63143bfd43cabc3bae831ccf93e186e8c
  commit 28c7062b041bcf2cf085d69e826d5b5827292a59.

Relevant durable prerequisites:
- boot-post-B162-rmfe-direct-multkey-trace-recode-candidate-2026-10-28.md
  blob abaceab3cc926a6a70b29c0aa695b477a93d171a;
- boot-RMFE-postdivide-turn15-dirty-lift-algorithm4-dividebyP-gate-2026-11-02.md
  blob f47a5008b1c810653b4f539ffd21c53ceb859230;
- boot-RMFE-postdivide-turn13-embedding-norm-certification-l1-rescue-gate-2026-11-03.md
  blob 91039eec2921b0c56d0b69042e40e1830ed1778d;
- boot-RMFE-postdivide-turn14-inverse-exit-cleanup-l1-envelope-gate-2026-11-03.md
  blob c09d29185d9f3e0941d313fcc8af560eb488dfc6;
- boot-RMFE-postdivide-turn16-pure-evalmap-scalar28-normalization-gate-2026-11-02.md
  blob 8335dc0648a890d3fad697726cb899946c00c51c;
- boot-RMFE-rm10-support-minimality-ten-automorphism-lower-bound-2026-11-01.md
  blob 48632b9bdf8887d241c7a4a9590f6c79459f0c59;
- boot-RMFE-postdivide-turn16-L0-L3-rho443-l1-envelope-gate-2026-11-03.md
  blob 07a0d58addfba66d3302ebf6cb42a2049ab51a76.

Pinned HElib source:
  homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

The target finding path was checked absent before write.

## Closest prior and exact delta

Closest external mechanisms remain:
- Geelen 2024/153 subring packing / coefficient-selection trace;
- Ma et al. 2024/164 RM_k and power-of-two BGV linear transforms;
- Aung et al. 2025/350 RMFE correction bootstrapping with k split MultKey executions.

The high-level direct-RMFE-MultKey goal is prior-disclosed by Aung.

The candidate-specific delta is now sharpened relative to Turn6:
the degree-8 envelope is used only as a sparse coefficient carrier.
A generic E8 SlotToCoeff / CoeffToSlots pair is NOT required.

Instead:
  RMFE projections
  -> sparse R8 coefficient envelope
  -> ONE ordinary coefficient-domain MultKey
  -> RM10
  -> one fused 8-Frobenius coefficient-to-RMFE recode
  -> Aung correction DigitExtract.

This simplification is enabled by the later durable arbitrary-Z625-lift theorem.

NOVELTY_STATUS remains PREFLIGHT.

## One primary hypothesis / falsifier

H7:
The old carry counterexample that killed the 2026-10-28 "raw inner-product -> recode" shortcut does not kill a revised order in which:
1. ONE MultKey first produces full Z625 coefficient lifts;
2. a public linear map then reconstructs arbitrary scalar Z625 lifts;
3. only THEN Aung correction Algorithm4 is invoked.

Falsifier:
if Aung correction DigitExtract requires canonical/high-digit representatives before the linear recode, or if the post-MultKey coefficient recode cannot produce exact arbitrary lifts of the original RMFE scalar components.

## 1. Why the old carry counterexample is narrower than the current theorem

The old objection used the fact that ordinary high p-adic digit extraction H is nonlinear:
  H(x+y) != H(x)+H(y)
in general.

Example:
  p=5,e=2,
  H(4)=0,
  H(1)=0,
  H(5)=1.

That counterexample remains valid.

What it forbids is:
  extract high digits on mixed coefficient/CRT states
  and then linearly reconstruct the desired scalar digits,
or equivalently commuting H through the linear mixing.

The new route never does that.

Turn15 later proved from Aung Algorithm4 that its correction procedure quantifies over arbitrary:
  a_i in Z_{p^e},
not only canonical F_p representatives.

Therefore it is sufficient to reconstruct ANY Z625 lift congruent to the intended scalar before Algorithm4.

This later theorem is a material reopen condition that was unavailable to the 2026-10-28 prescout.

## 2. Exact sparse R8 input representation

Let:
  S=Z/625Z,
  R8=S[Y]/(Y^16+1),
  Y=X^1024.

The two physical slots correspond to roots zeta and zeta^{-1}.
Let:
  I=zeta^8 in S,
so:
  I^2=-1 mod625.

The two roots are:
  I=182 or443.
Take balanced:
  I=182,
while the second slot sees -I.

For RMFE component i, let the desired physical scalar slots be:
  a_{i,+}, a_{i,-} in S.

The scalar-packed branch tau_i(c) in R8 has the unique coefficient pair:
  b_i=(a_{i,+}+a_{i,-})/2,
  c_i=(a_{i,+}-a_{i,-})/(2I),
so:
  b_i + I c_i = a_{i,+},
  b_i - I c_i = a_{i,-}.

Define directly:
  A(c)=sum_{i=0}^4 Y^i tau_i(c).

Hence A(c) has only ten potentially nonzero R8 coefficients:
  coefficient i     = b_i,
  coefficient i+8   = c_i,
for i=0,...,4.

No E8 SlotToCoeff is required to create a coefficient-domain plaintext.
The ciphertext already encrypts the relevant ten coefficient values in the full ring.

## 3. ONE MultKey on the sparse coefficient representation

Run the ordinary HElib MultKey middle directly on A(c):
  canonicalize/relinearize-to-recrypt-key
  -> rawModSwitch
  -> newMakeDivisible
  -> exact /p^{e'}
  -> one recryptEkey reconstruction.

This stage is coefficient-domain and does not require the coefficients to equal the final application scalars; it only requires the standard HElib recryption semantic invariant.

Conditioned on the standard MultKey correctness event, after reconstruction and coefficient selection the retained coefficients z_t satisfy:
  z_i     == b_i mod625,
  z_{i+8} == c_i mod625.

They need not be canonical integer representatives.

## 4. RM10 recovers exactly the embedded R8 support

Use the existing ten-stage unnormalized trace:
  T_H = sum_{h in H} sigma_h,
where:
  H={u mod32768 : u=1 mod32},
  |H|=1024.

T_H keeps exactly X^(1024t) coefficients and kills all other coefficient positions.

Do NOT physically multiply by 224 at this point.

Semantically:
  T_H = 1024 * P_H.

Because 1024 is a unit modulo625, the missing normalization can be absorbed later through HElib's BGV scalar-unit metadata path.

This avoids an unnecessary physical error multiplier.

## 5. Exact scalar-coordinate recovery inside R8

Let sigma be the R8 Frobenius:
  sigma(Y)=Y^5.

The subgroup <sigma> has order8 and fixes the scalar-packed subring:
  S[Y^8]/(Y^16+1).

Define the unnormalized trace:
  T_8 = sum_{j=0}^7 sigma^j.

Exact monomial identity:
  T_8(Y^t)=
    8 Y^t, for t in {0,8},
    0, otherwise.

For each i=0,...,4:
  s_i := T_8(Y^{-i} Z)
       = 8*(z_i + z_{i+8}Y^8).

In the two physical slots:
  s_i(+)=8*(z_i + I z_{i+8}),
  s_i(-)=8*(z_i - I z_{i+8}).

Modulo625:
  z_i +/- I z_{i+8}
  == b_i +/- I c_i
  == a_{i,+/-}.

Thus after removing the common unit8, these are exact arbitrary Z625 lifts of the intended scalar components.

No high-digit extraction has been commuted through the mixing.

## 6. Fused RMFE recode

Use the frozen RMFE basis elements:
  phi_i(X)=sum_{k=0}^4 ell_{i,k} X^(16k),

with:
  ell_0=[1,50,340,260,599]
  ell_1=[0,4,204,314,104]
  ell_2=[0,622,161,623,469]
  ell_3=[0,418,206,522,104]
  ell_4=[0,156,339,156,599].

Define the unnormalized fused map:
  G(Z)=sum_{i=0}^4 phi_i * T_8(Y^{-i} Z).

Equivalently:
  G(Z)=sum_{j=0}^7 D_j sigma^j(Z),

where:
  D_j = sum_{i=0}^4 phi_i * sigma^j(Y^{-i}).

Exact full-ring arithmetic modulo X^16384+1 and625 gives, for every j=0,...,7:
  #nonzero coefficients(D_j)=21,
  max balanced coefficient magnitude=311,
  ||D_j||_1=2811.

Therefore:
  A_G := sum_j ||D_j||_1
       = 8*2811
       = 22488.

Exact basis audit:
for every one of the 16 R8 coefficient basis monomials Y^t,
the formula above equals:
  8 * sum_{i=0}^4 phi_i * (coefficient-pair i extracted from Y^t).

Hence by S-linearity the identity holds for every Z in R8.

## 7. One final scalar-unit normalization handles BOTH traces

The RM10 trace contributes semantic scale:
  1024.

The R8 scalar-coordinate trace contributes semantic scale:
  8.

Combined:
  8192 mod625.

Exact inverse:
  8192^{-1} mod625 = 28.

Therefore canonical implementation is:

  one MultKey reconstruction
  -> unnormalized RM10 trace
  -> cleanUp
  -> unnormalized fused recode G
  -> cleanUp
  -> ctxt.multByConstant(28L)
  -> Aung correction DigitExtract.

Pinned HElib BGV scalar-unit path for c=28:
  gcd(28,625)=1,
  physically multiplies ciphertext parts by1,
  changes only intFactor by28^{-1}=67,
  adds ZERO direct noiseBound multiplication.

Thus both trace normalizations are absorbed by ONE capacity-free scalar-unit metadata operation.

The resulting semantic plaintext is:
  sum_i phi_i * a'_i,
where every a'_i is an arbitrary Z625 lift congruent to the original RMFE scalar.

Turn15 therefore applies directly.

## 8. Exact one-reconstruction absolute L1 envelope

Conditioned on successful rawModSwitch/newMakeDivisible for the ONE merged ciphertext, the persisted hard source bound gives every post-divide public polynomial coefficient:
  |c_j|<=313.

For one path:
  S0,S1 <= 16384*313
        = 5,128,192.

Turn13 independent recryptEkey coefficient-L1 envelope:
  N_E <=271,351,808.

Worst BGV addConstant factor:
  |f|<=312.

Hence the one reconstruction satisfies:
  E_rec
    <= N_E*S1 + |f|*S0
    <= 1,391,545,770,967,040.

log2(E_rec) <=50.3056097861.

This is five times smaller in the public-polynomial L1 factor than the old five-branch shared-reconstruction guard.

## 9. RM10 source-faithful independent envelope

Use the source-sized one-hop automorphism key-switch envelope:
  K <=401,679,183,790,909.

Use the special-prime cleanup rounding envelope:
  R <=83,891,200,000.

RM10 has ten stages:
  x <- x + sigma_{u_t}(x).

At the first stage the input is on ctxtPrimes:
- one automorphism/key-switch contributes K;
- no prior special-prime drop is needed.

After that the accumulator carries special primes.
At every later smartAutomorph, pinned reLinearize first drops special primes and then key-switches:
- fresh normalized contribution <=R+K.

The physical RM10 remains UNNORMALIZED, so the original existing error is amplified by at most:
  2^10=1024.

Fresh error injected at stage t is amplified by at most the remaining powers of2.

After the ten stages, perform one explicit cleanUp.

Therefore:
  E_RM10
    <= 1024*E_rec
       + 1023*K
       + 512*R
    <= 1,835,903,626,782,748,867.

log2(E_RM10) <=60.6711960364.

No factor224 multiplies this error because normalization is deferred to the final scalar-unit28 path.

## 10. Fused recode independent envelope

Start the fused map from the cleaned RM10 output on ctxtPrimes.

Implement the seven nonidentity Frobenius images using the already-established direct FULL temporary-625 Frobenius matrices.

All eight D_j satisfy:
  ||D_j||_1=2811.

Existing-error contribution:
  <=22488 * E_RM10.

Each of the seven nonidentity Frobenius key switches contributes at most K before its public D_j multiplier:
  fresh <= 7*2811*K.

After summing, perform one explicit cleanUp:
  +R.

Thus:
  E_preDE
    <=22488*E_RM10
      +7*2811*K
      +R
    <=41,293,704,600,473,801,437,489.

log2(E_preDE)
  <=75.1283399410.

With bits_HElib=400:
  log2(Q)>=399.5.

Hence:
  log2(Q/E_preDE)
  >=324.3716600590 bits.

Against the current-ring correctness threshold0.48Q:
  margin
  >=323.3127663700 bits.

This is an independent coefficient-L1 correctness margin immediately BEFORE Aung correction DigitExtract, conditioned on the merged rawModSwitch correctness event and the source-sized K/R assumptions.

## 11. Optional public L0-L3 stress check

Turn16's worst public correction amplification is:
  A3=653905.

Even multiplying the pre-DigitExtract envelope by A3 gives:
  log2(E_L3) <=94.4470614701

and still leaves:
  >=303.9940448408 bits
above the 0.48Q linear correctness threshold.

This does NOT prove the downstream nonlinear Algorithm4 trajectory; it only shows the public L0-L3 front edge is nowhere near the static correctness boundary.

## 12. Construction supersession

SUPERSEDE Turn6 canonical construction:

OLD:
  A(c)
  -> generic lifted E8 SlotToCoeff
  -> ONE MultKey
  -> RM10
  -> lifted E8 CoeffToSlots
  -> eight-coordinate unpack
  -> RMFE recombination
  -> DigitExtract.

NEW:
  A(c) already sparse in R8 coefficient basis
  -> ONE MultKey DIRECTLY
  -> unnormalized RM10
  -> one fused unnormalized 8-Frobenius RMFE recode
  -> scalar-unit28 normalization
  -> DigitExtract.

The old generic E8 maps remain algebraically implementable, but they are no longer part of the canonical candidate.

This is a material constructive simplification:
- removes both generic degree-8 transforms;
- removes explicit 8-output unpack;
- uses one 8-term fused linearized map;
- leaves final intFactor=67, already covered by the prior Algorithm4 unit-closure theorem.

## 13. Remaining blocker

This turn's absolute envelope starts AFTER successful rawModSwitch/newMakeDivisible.

The unresolved candidate-specific precondition is now sharply isolated:

  five RMFE projections
  -> A(c)=sum Y^i tau_i(c)
  -> relinearize to recrypt key
  -> merged rawModSwitch.

The merge adds at most:
  sum_i B_i <=5 max_i B_i
to a deterministic branch-error envelope before rawModSwitch.

But no provenance-complete absolute pre-raw branch envelope B_i has yet been instantiated for the new single-ciphertext path.

Therefore:
  MERGED_RAWMODSWITCH_CORRECTNESS = PENDING.

This is the next decisive static gate.

## Verdict

PASS_DIRTY_LIFT_SUPERSESSION_OF_OLD_CARRY_OBJECTION.
PASS_DIRECT_R8_COEFFICIENT_MULTKEY_CONSTRUCTION.
PASS_EXACT_FUSED_8_FROBENIUS_RECODE.
PASS_COMBINED_8192_SCALAR_UNIT28_NORMALIZATION.
PASS_POST_RAW_ABSOLUTE_L1_PRE_DIGITEXTRACT_MARGIN.
MERGED_RAWMODSWITCH_CORRECTNESS=PENDING.

Candidate remains ACTIVE.
Phase remains CONSTRUCTIVE_DESIGN until the merged pre-raw gate is closed.

Novelty=PREFLIGHT.
Security=PENDING.
Value=PENDING.
Baseline correctness=PENDING.
Audit=PENDING.
Paper readiness=NOT_READY.

## Next decisive Paper-First test

NO Native.

Recover/derive an absolute source-faithful pre-raw error envelope for the five Aung Method-1 RMFE projections tau_i and their merged sparse envelope:
  A(c)=sum_i Y^i tau_i(c).

Propagate that envelope through the single:
  reLinearize(recryptKeyID)
  -> mod-down
and test HElib's rawModSwitch correctness/noise condition for the merged ciphertext.

The decisive question is whether the at-most5x branch merge penalty still leaves a certified rawModSwitch margin under p=5,m=32768,bits=400.

If this gate fails and requires another structural redesign, PARK the candidate.

No Native action is authorized by this finding.


## Independent re-derivation verification — same logical Turn 7

This block is a verification companion, NOT a new counted research turn.

Authority used for the calculation: fixed snapshot
`fdbf8ccf92b4751a4cc9678f5ef9c26ac64c48f4`.
The already-present current-main Turn-7 body was treated only as a coordination artifact, not as the source of these calculations.

Fixed prerequisite blobs from that snapshot:
- `findings/boot-RMFE-r8-exact-plaintext-map-generator-2026-10-29.md` — `3b6ec1888d738add2f65dee239c1972db0be3fd4`;
- `findings/boot-RMFE-rank5-shared-correction-exact-moore-norm-gate-2026-10-31.md` — `d7583ac052daefafc3fd1858bbecf67005c1fa10`;
- `findings/boot-RMFE-postdivide-turn13-embedding-norm-certification-l1-rescue-gate-2026-11-03.md` — `91039eec2921b0c56d0b69042e40e1830ed1778d`;
- `findings/boot-RMFE-postdivide-turn14-inverse-exit-cleanup-l1-envelope-gate-2026-11-03.md` — `c09d29185d9f3e0941d313fcc8af560eb488dfc6`;
- `findings/boot-RMFE-postdivide-turn15-dirty-lift-algorithm4-dividebyP-gate-2026-11-02.md` — `f47a5008b1c810653b4f539ffd21c53ceb859230`;
- `findings/boot-RMFE-postdivide-turn16-pure-evalmap-scalar28-normalization-gate-2026-11-02.md` — `8335dc0648a890d3fad697726cb899946c00c51c`.

### Exact arithmetic checks

Over `S=Z/625Z`:
- `182^2 = 443^2 = -1 mod 625`;
- `1024^{-1}=224 mod625`;
- `8192^{-1}=28 mod625`;
- `28^{-1}=67 mod625`.

Frozen RMFE basis:
`ell_0=[1,50,340,260,599]`,
`ell_1=[0,4,204,314,104]`,
`ell_2=[0,622,161,623,469]`,
`ell_3=[0,418,206,522,104]`,
`ell_4=[0,156,339,156,599]`.

For
`D_j=sum_{i=0}^4 phi_i * sigma^j(Y^{-i})`, `j=0,...,7`,
independent sparse full-ring arithmetic modulo `X^16384+1` and 625 gives:
- every `D_j`: 21 nonzero coefficients;
- every `D_j`: centered coefficient infinity norm 311;
- every `D_j`: exact coefficient-L1 norm 2811;
- aggregate `sum_j ||D_j||_1 = 22488`.

Canonical JSON encoding of all eight exact sparse `D_j` coefficient dictionaries has:
`SHA256 = 7b0a2a5c004cd02c20d259dd444d0234e909ea93ba75d45ffd3e941392df3581`.

Basis proof was independently recomputed for all `t=0,...,15`:
`G(Y^t)=8 phi_t` for `0<=t<=4`;
`G(Y^t)=8 phi_{t-8}Y^8` for `8<=t<=12`;
and `G(Y^t)=0` for padding coordinates `t in {5,6,7,13,14,15}`.
Result: `16/16 PASS`.

### Independent absolute-L1 recomputation

Using the fixed deterministic constants
`N_E=271351808`,
`S0=S1=16384*313=5128192`,
`|f|<=312`,
`K=401679183790909`,
`R=83891200000`:

`E_rec = N_E*S1 + 312*S0 = 1391545770967040`,
`log2(E_rec)=50.30560978613817`.

For unnormalized RM10:
`E_RM10 = 1024*E_rec + 1023*K + 512*R
          = 1835903626782748867`,
`log2(E_RM10)=60.67119603643458`.

For the fused 8-Frobenius recode followed by one cleanup:
`E_preDE = 22488*E_RM10 + 7*2811*K + R
          = 41293704600473801437489`,
`log2(E_preDE)=75.12833994098358`.

With `log2(Q)>=399.5`, the independent margin to the `0.48Q` sufficient correctness threshold is:
`323.3127663699629 bits`.

Applying the current worst public Algorithm-4-entry linear amplification
`A3=653905` gives:
`log2(A3*E_preDE)=94.44706147012812`,
with remaining `0.48Q` margin:
`303.99404484081833 bits`.

These calculations verify the Turn-7 post-raw conclusion and do not close the remaining merged pre-raw rawModSwitch gate.
