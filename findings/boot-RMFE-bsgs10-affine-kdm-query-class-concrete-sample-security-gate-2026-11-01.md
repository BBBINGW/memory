# BOOT RMFE BSGS+10 Affine-KDM Query-Class / Concrete-Sample Security Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 21/25
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

\`BBBINGW/memory main@3d50ea00099489024d6371ab3b16a2f017bd4a54\`.

Relevant durable prerequisites:
- Turn 10 BSGS+10 evaluation-key security-assumption gate;
- Turn 3 Part 2 exact +10-matrix / +5.555556% Frobenius-row overhead;
- Aung's explicit circular-security posture.

## Primary hypothesis

The ten additional same-key RM10 automorphism hints may require a formally stronger KDM function class, or may materially change concrete lattice security simply because the public evaluation-key row count grows from \(180D\) to \(190D\).

Falsifier:
show that:
1. each automorphism hint is already an affine/linear function of the coefficient-vector secret;
2. standard affine-KDM security is defined for polynomially many oracle queries from the whole affine class;
3. the plain-LWE estimator sample parameter is not, by itself, a faithful model of HElib's secret-dependent KeySwitch hints.

## 1. Automorphism of the ring secret is an affine KDM function

Represent the secret polynomial

\[
s(X)=\sum_{i=0}^{N-1}s_iX^i
\]

by its coefficient vector

\[
\mathbf s\in R^N
\]

over the relevant residue ring.

For \(u\in\mathbb Z_m^\*\), the ring automorphism

\[
\sigma_u:s(X)\mapsto s(X^u)
\]

is an \(R\)-linear permutation/sign-linear transform on the coefficient module:

\[
\boxed{
\sigma_u(\mathbf s)=A_u\mathbf s
}
\]

for a public matrix \(A_u\).

Thus each HElib same-key automorphism KeySwitch hint encrypts/noisily encodes a zero-constant affine function of the secret.

Turn 10's exact row relation was:

\[
b_{u,j}+a_{u,j}s
=
P_j\sigma_u(s)+p_{\rm KS}e_{u,j}.
\]

So the secret-dependent message family used by the ten RM10 matrices is not nonlinear in \(s\).

## 2. Standard affine-KDM class already contains all ten functions

The KDM literature defines security by allowing an adversary to request encryptions of functions of the secret key from a prescribed family.

Public sources summarizing ACPS09 state that the LWE-based construction achieves KDM security for affine functions; later KDM formulations explicitly allow polynomially many KDM encryption queries.

Therefore, if one adopts the broad function class

\[
\mathcal F_{\rm aff}
=
\{
\mathbf s\mapsto A\mathbf s+\mathbf b
\},
\]

then every stock BSGS automorphism and every added RM10 automorphism already belongs to the same class.

Under that broad formulation, changing from 180 direct Frobenius automorphisms to 190 does **not** enlarge the KDM function class:

\[
\boxed{
\mathcal F_{\rm stock}
=
\mathcal F_{\rm cand}
=
\mathcal F_{\rm aff}
}
\]

at the class level.

It only changes the number of concrete KDM queries/hints published.

Thus Turn 10's phrase

\`UNCLEAR_FORMAL_KDM_FUNCTION_FAMILY_EXTENSION\`

was overly conservative if the assumed KDM class is all affine functions.

The correct distinction is:

- **finite enumerated function set model:** \(180\to190\) functions;
- **all-affine KDM class model:** same class, ten additional queries.

## 3. Polynomial-query closure means +10 is asymptotically immaterial

Standard KDM games permit polynomially many oracle queries.

The HElib context dimension, digit count, and number of evaluation keys are polynomial in the security parameter.

Adding ten automorphism matrices adds:

\[
10D
\]

KeySwitch rows.

Hence under an affine-KDM assumption that already supports polynomially many queries,

\[
\boxed{
180D\to190D
}
\]

does not create a new asymptotic assumption.

This is stronger than merely saying "same relation type":

> under broad affine-KDM-with-polynomial-queries, the candidate stays inside the same function class and the same polynomial-query regime.

## 4. This does NOT prove HElib from ACPS09

The above classification is about the **shape of the assumption**, not a reduction for HElib.

ACPS09-style LWE KDM-secure encryption is a particular PKE construction and proof.

HElib's BGV KeySwitch matrix has its own structure:
- digit-scaled source-secret term \(P_j\sigma_u(s)\);
- target-secret RLWE row;
- special-prime/digit decomposition;
- ring setting;
- bootstrapping key cycle involving \(s_R\).

No source inspected in this turn proves that HElib's exact evaluation-key distribution is an instance of the ACPS09 KDM-secure encryption theorem.

Therefore:

\[
\boxed{
\text{AFFINE-KDM CLASSIFICATION}
\neq
\text{FORMAL HElib KDM REDUCTION}.
}
\]

A future paper may cite affine-KDM literature to explain that the added automorphisms are not a more expressive secret-function class, but should still state security under the evaluation-key/circular assumptions already used by HElib/Aung.

## 5. Aung's "circular security" statement is narrower language

Aung physical p9 describes the bootstrapping key as an encryption of the secret key under itself "assuming circular security."

That statement directly addresses the self-encryption cycle used by bootstrapping.

It does not spell out a formal affine-KDM theorem covering every HElib automorphism/relinearization hint.

Yet stock HElib already exposes many such same-key secret-dependent evaluation keys.

So the safe paper posture remains:

> same HElib evaluation-key / circular-KDM posture, with ten additional standard same-key automorphism hints.

Do not rewrite Aung's sentence into a theorem they did not state.

## 6. Plain-LWE estimator sample count is a separate model

Modern lattice-estimator interfaces expose a parameter

\[
m
\]

defined as the number of LWE samples available to the attacker, and allow even

\[
m=\infty.
\]

Thus for ordinary message-independent LWE, finite sample count can affect concrete attack estimates.

However HElib automorphism KeySwitch rows are not plain zero-message LWE samples:

\[
b_{u,j}+a_{u,j}s
=
P_jA_u s + p e_{u,j}.
\]

The right-hand side contains another public linear function of the **same secret**.

Without a justified KDM-to-plain-LWE reduction, one cannot simply count these rows as \(190D\) ordinary independent LWE samples and feed that number into a standard LWE estimator.

Therefore Turn 10's

\`UNCLEAR_CONCRETE_SAMPLE_COUNT_SECURITY\`

should be refined:

\[
\boxed{
\text{the main blocker is model mismatch, not lack of row counting}.
}
\]

The row count itself is exact.

## 7. Unlimited-sample estimator observation

The current lattice-estimator documentation uses an \(m\) parameter for attacker-available samples and permits \(m=\infty\); the documented default is unlimited samples.

Consequently, **if** Aung's reported 100-bit estimate used an unlimited-sample LWE model, then increasing the number of available plain-LWE samples from an already-sufficient finite number would not change that estimator input at all.

But Aung only cites Albrecht–Player–Scott 2015 and reports "at least 100-bit security"; the paper does not publish:
- the estimator code/version;
- exact \(m\);
- attack list;
- secret/error distributions supplied to the estimator;
- whether evaluation-key rows were modeled.

Hence:

\[
\boxed{
\text{Aung's 100-bit claim cannot be numerically updated from the paper alone}.
}
\]

## 8. 5.555556% row growth is not a 5.555556% security loss

The exact row increase is:

\[
\frac{190D-180D}{180D}
=
5.555556\%.
\]

There is no valid rule:

\[
\Delta\text{security bits}
=
-5.555556\%.
\]

Lattice attack cost is nonlinear in \(n,q,\alpha,m\), and KDM hints have additional structure.

Therefore any statement such as:

> "key security decreases by about 5.6%"

is invalid.

Likewise, Turn 3's exact +5.56% byte overhead must not be conflated with security loss.

## 9. Security claim boundary after this turn

### Safe

> The ten added RM10 keys are standard HElib same-key automorphism switching hints and encode linear/affine functions of the existing secret. Under an affine-KDM model supporting polynomially many queries, they do not enlarge the secret-function class or query asymptotics.

### Safe

> The key-dependency graph and ciphertext parameters are unchanged.

### Safe

> The candidate adds \(10D\) evaluation-key rows, exactly +5.555556% relative to the stock BSGS Frobenius-row count.

### Unsafe

> HElib is formally affine-KDM secure by ACPS09.

No reduction was established.

### Unsafe

> Standard RLWE security is unchanged.

The evaluation keys are secret-dependent hints, not ordinary message-independent RLWE ciphertexts.

### Unsafe

> +10 keys have exactly zero concrete security effect.

Not established unless a specific security model/estimator already assumes unlimited relevant samples and adequately models the hints.

## 10. Reopening condition after systems PASS

If the pending systems task Strong-PASSES, the next security work should be chosen according to claim ambition.

### For a systems/implementation paper

Likely sufficient:
- retain same HElib/Aung circular/evaluation-key assumption;
- state +10 standard automorphism hints;
- report unchanged ring/modulus/secret parameters;
- avoid claiming a new formal reduction.

### For a stronger cryptographic security theorem

Need a separate proof that HElib/BGV's concrete KeySwitch/recrypt hint distribution is simulatable/KDM-secure for the required affine related-secret functions and two-key cycle.

That is a distinct research problem and should not be implied by lattice-estimator output.

## Verdict

\`\`\`text
RESULT:
  PASS_AFFINE_KDM_CLASS_UNCHANGED
  PASS_POLYNOMIAL_QUERY_REGIME_UNCHANGED
  FAIL_PLAIN_LWE_SAMPLE_COUNT_AS_FORMAL_KDM_MODEL

AUTOMORPHISM_SECRET_FUNCTION:
  LINEAR / AFFINE
  sigma_u(s) = A_u s

BROAD_AFFINE_KDM_FUNCTION_CLASS:
  UNCHANGED

CONCRETE KDM QUERIES:
  +10 MATRICES
  +10D ROWS

QUERY ASYMPTOTICS:
  UNCHANGED / POLYNOMIAL

KEY_DEPENDENCY_GRAPH:
  UNCHANGED

FORMAL ACPS09 -> HELib REDUCTION:
  NOT ESTABLISHED

PLAIN_LWE ESTIMATOR m:
  RELEVANT TO ORDINARY LWE SAMPLE MODEL
  NOT AUTOMATICALLY A MODEL OF SECRET-DEPENDENT HINTS

LATTICE-ESTIMATOR DEFAULT:
  ALLOWS / DOCUMENTS m = infinity

AUNG ESTIMATOR m:
  UNKNOWN

AUNG 100-BIT NUMERICAL UPDATE:
  NOT POSSIBLE FROM PUBLISHED DETAILS

5.555556% ROW INCREASE:
  NOT A SECURITY-BIT LOSS PERCENTAGE

SECURITY POSTURE:
  SAME HElib/AUNG EVALUATION-KEY/CIRCULAR-KDM POSTURE
  WITH TEN ADDITIONAL STANDARD AUTOMORPHISM HINTS

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Turn 21 removes one unnecessary ambiguity from Turn 10.

The ten RM10 automorphisms do not require a more expressive secret-function family if security is stated using the standard affine-KDM class with polynomially many queries.

What remains unresolved is not the function class but the absence of a formal theorem connecting HElib's exact BGV evaluation-key distribution and bootstrapping cycle to such a KDM-secure construction.

For the likely systems-paper path, the defensible security claim is therefore inheritance of the existing HElib/Aung evaluation-key/circular-security posture, not a new standard-RLWE proof.
