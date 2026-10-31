# BOOT RMFE BSGS+10 Evaluation-Key Security-Assumption Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 10/25
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

\`BBBINGW/memory main@f3aeea7309bfa08e176ac57f4a5ef88d823843a1\`.

Relevant durable prerequisites:
- Turn 3: BSGS Frobenius direct-key count 180; adding ten direct RM10 targets gives 190;
- Turn 3 Part 2: all ten added matrices have exactly the same stored geometry as ordinary same-context Frobenius matrices;
- Turn 7: under equal BSGS+10 keysets, Corr./TnM uses two of the ten added matrices, but the candidate uses all ten.

## Primary hypothesis

Adding the ten direct RM10 automorphism matrices may create a new security assumption or a qualitatively new key-dependent leakage channel beyond the stock HElib/Aung bootstrapping setup.

Falsifier:
show that the added matrices:
- use the exact same HElib \`GenKeySWmatrix(1,k,keyID,keyID)\` relation as stock Frobenius keys;
- introduce no new secret-key ID, source-key power, target-key family, ring, or plaintext-space policy;
- add only more instances/functions inside an already-present automorphism-key family.

## Source provenance

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/keySwitching.cpp:528-617\`: standard BSGS Frobenius matrix generation;
- \`src/keySwitching.cpp:688-696\`: \`addTheseMatrices\`;
- \`src/keys.cpp:1152-1238\`: \`GenKeySWmatrix\`;
- \`src/keys.cpp:1671-1705\`: \`genRecryptData\`.

Aung et al. ePrint 2025/350 mirror:
- VERSION_UNVERIFIED;
- SHA256 \`922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82\`;
- physical p9 explicitly describes the bootstrapping key as an encryption of the secret key under itself "assuming circular security";
- physical p23 reports an estimated at-least-100-bit security level using the Albrecht et al. lattice estimator for their HElib parameters.

The p23 estimator statement does not by itself constitute a proof of circular/KDM security.

## 1. Exact relation represented by a same-key automorphism matrix

For

\[
\texttt{GenKeySWmatrix}(1,u,0,0),
\]

HElib sets

\[
s_u=\sigma_u(s_0)=s_0(X^u).
\]

For each digit row \(j\), \`RLWE1\` first creates an RLWE sample under target secret \(s_0\):

\[
b_j+a_js_0=p_{\rm KS}e_j.
\]

Then HElib adds the appropriate digit-scaled source secret \(s_u\) to \(b_j\).

Therefore each final row has the form

\[
\boxed{
b_{u,j}+a_{u,j}s_0
=
P_j\,\sigma_u(s_0)+p_{\rm KS}e_{u,j},
}
\]

where \(P_j\) is the public digit/special-prime scaling factor.

So an automorphism key is a noisy encryption/hint of the secret-dependent linear function

\[
\sigma_u(s_0)
\]

under the same main secret \(s_0\).

This is a KDM/related-secret style relation; it is not ordinary message-independent IND-CPA ciphertext material.

## 2. Stock BSGS already publishes the same relation family

Pinned \`addBSGSFrbMatrices\` calls the same matrix generator:

\[
\texttt{GenKeySWmatrix}(1,\operatorname{genToPow}(-1,j),0,0)
\]

for:
- 90 baby Frobenius exponents;
- 90 giant Frobenius exponents.

Thus the stock BSGS Frobenius public key already contains

\[
\boxed{180}
\]

same-key automorphism hints of exactly the form above.

The ten RM10 additions are generated through \`addTheseMatrices\`, which again executes only

\[
\texttt{GenKeySWmatrix}(1,k,0,0).
\]

Therefore every added RM10 key has:
- \`fromSPower=1\`;
- \`fromIdx=0\`;
- \`toIdx=0\`;
- same target secret \(s_0\);
- same BGV key-switch plaintext-space policy;
- same ring/modulus context;
- same digit decomposition geometry.

Only the automorphism exponent \(u\) changes.

## 3. Exact key-dependency graph is unchanged

HElib bootstrapping already contains two secret-key identities:

\[
s_0
\quad\text{and}\quad
s_R.
\]

Pinned \`genRecryptData\` generates:

1. \`GenKeySWmatrix(1,1,0,R)\`:
   a key-switch hint containing digit-scaled \(s_0\) under target key \(s_R\);

2. \`recryptEkey = Encrypt_{s_0}(s_R)\`:
   an encryption of the recryption secret \(s_R\) under \(s_0\).

Hence the implementation already has the two cross-key dependencies

\[
s_0 \text{ under } s_R
\quad\text{and}\quad
s_R \text{ under } s_0,
\]

i.e. an existing two-key circular dependency at the implementation level.

Stock automorphism/relinearization keys additionally create same-key secret-function loops under \(s_0\).

The ten RM10 matrices add only ten further same-key automorphism-function loops:

\[
\sigma_{u_1}(s_0),\ldots,\sigma_{u_{10}}(s_0)
\quad\text{under }s_0.
\]

They introduce:
- no new secret-key vertex;
- no new cross-key edge;
- no new secret power \(s_0^r\);
- no new ring;
- no new modulus family.

Thus:

\[
\boxed{
\text{the key-dependency graph topology is unchanged}.
}
\]

## 4. Security-assumption classification

Aung's paper-level bootstrapping discussion already invokes circular security.

HElib's stock BSGS implementation already publishes a large family of automorphism switching hints depending on \(s_0\).

Therefore the candidate does **not** introduce a qualitatively new kind of secret-dependent public material.

The strongest safe statement is:

> Under the same HElib/Aung evaluation-key model that already accepts stock Frobenius automorphism keys and circular bootstrapping material, BSGS+10 adds more instances of the existing automorphism-key relation type, rather than a new relation type.

However, one must distinguish this from a formal theorem that the assumption is literally unchanged.

If a formal KDM assumption is parameterized by a fixed function family

\[
\mathcal F_{\rm BSGS}
=
\{\sigma_u:u\in U_{\rm BSGS}\},
\]

then the candidate uses the enlarged family

\[
\mathcal F_{\rm cand}
=
\mathcal F_{\rm BSGS}
\cup
\{\sigma_{u_1},\ldots,\sigma_{u_{10}}\}.
\]

So in a narrowly function-scoped formalization, ten additional functions are indeed authorized.

This is a **function-family extension**, not a new KDM function class.

If the assumed model grants security for arbitrary polynomially many same-key automorphism functions, then no qualitative assumption change occurs.

No source inspected in this turn proves that exact KDM theorem for HElib's concrete BGV implementation.

## 5. Sample-count effect

Let

\[
D=|\texttt{context.getDigits()}|.
\]

Every KeySwitch matrix stores \(D\) RLWE-style rows.

Hence the BSGS Frobenius family contributes

\[
180D
\]

rows, while BSGS+10 contributes

\[
190D.
\]

The candidate therefore adds exactly

\[
10D
\]

same-key automorphism-key RLWE rows, i.e.

\[
\boxed{+5.555556\%}
\]

relative to the stock BSGS Frobenius-row count.

This matches the exact dominant DCRT-payload ratio from Turn 3 Part 2.

But security loss is not linear in sample count.

More RLWE/KDM samples can in principle affect concrete lattice-attack cost, and the Aung p23 "at least 100-bit" statement does not expose enough estimator configuration to determine whether:
- evaluation-key rows were counted as attacker samples;
- an effectively-unlimited-sample model was used;
- circular/KDM security was modeled at all.

Therefore:

\[
\boxed{
\text{exact concrete-bit security effect of +10D rows is unresolved}.
}
\]

## 6. Why the published 100-bit estimate does not close this gate

Aung reports:
- \(m=32768\);
- \`bits=400\`;
- maximum ciphertext bit-width 538--541;
- estimated security at least 100 bits via the lattice estimator.

That is useful parameter evidence.

It is not evidence that:
- HElib BGV is formally circular/KDM secure;
- all automorphism-key function families reduce to plain RLWE;
- changing 180 to 190 automorphism keys has exactly zero concrete-security effect.

So the candidate should inherit Aung's **security-assumption posture**, not overclaim a stronger proof.

## 7. Security disposition for a future paper

If the pending systems gate succeeds, the security section should state approximately:

1. the ciphertext/RLWE parameters are unchanged;
2. no new secret-key identity or secret-key cycle is introduced;
3. the construction adds ten standard HElib same-key automorphism switching matrices;
4. these have the same form as the existing BSGS Frobenius evaluation keys;
5. security is therefore conditional on the same circular/evaluation-key KDM posture already required by the underlying HElib bootstrapping implementation, with an enlarged finite automorphism-function set;
6. concrete lattice security should be re-estimated with the actual evaluation-key sample count if the estimator model supports it.

Do **not** write:

\`security is unchanged under standard RLWE alone\`

unless a separate formal reduction is established.

## Verdict

\`\`\`text
RESULT:
  PASS_NO_NEW_KEY_DEPENDENCY_GRAPH
  PASS_SAME_AUTOMORPHISM_KEY_RELATION_TYPE
  UNCLEAR_FORMAL_KDM_FUNCTION_FAMILY_EXTENSION
  UNCLEAR_CONCRETE_SAMPLE_COUNT_SECURITY

STOCK_BSGS_FROBENIUS_KEYS:
  180

CANDIDATE_BSGS_PLUS10:
  190

ADDED_RELATION_TYPE:
  GenKeySWmatrix(1,u,0,0)
  SAME AS STOCK FROBENIUS KEYS

NEW_SECRET_KEY_ID:
  NO

NEW_CROSS_KEY_DEPENDENCY:
  NO

NEW_SECRET_POWER:
  NO

KEY_DEPENDENCY_GRAPH_TOPOLOGY:
  UNCHANGED

AUTOMORPHISM_KDM_FUNCTION_SET:
  +10 FUNCTIONS

RLWE_ROWS_ADDED:
  +10D
  +5.555556% RELATIVE TO BSGS FROBENIUS ROWS

AUNG PAPER SECURITY POSTURE:
  CIRCULAR SECURITY ASSUMED FOR BOOTSTRAPPING

AUNG REPORTED PARAMETER SECURITY:
  >=100 bits via lattice estimator
  DOES NOT PROVE CIRCULAR/KDM SECURITY

PLAIN-RLWE-ONLY SECURITY CLAIM:
  NOT ESTABLISHED

CANDIDATE_SECURITY_BLOCKER:
  NO QUALITATIVELY NEW ASSUMPTION FOUND
  FORMAL/CONCRETE QUANTIFICATION STILL CONDITIONAL

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

BSGS+10 does not create a new circular-security topology or a new HElib evaluation-key primitive.

Its security cost is best understood as:
- ten more functions in the already-used same-key automorphism/KDM family;
- \(10D\) more RLWE-style evaluation-key rows.

This removes a qualitative security blocker, but not the need for honest assumption wording or eventual concrete-security re-estimation if the systems result justifies publication work.
