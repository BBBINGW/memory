# BOOT RMFE Raw-Success-to-Digit-Norm Deterministic-Bound Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 9/25
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

\`BBBINGW/memory main@f207cfc91d0b47d100b7bca7517c55d0fac104ce\`.

Turn 8 killed scalar-only HElib \`noiseBound\` domination and left two deterministic reopening ideas:

- Route A: derive a source-shaped analytic bound on every later \`breakIntoDigits\` norm;
- Route C: derive such a bound directly from the successful rawModSwitch envelope / recryption noise condition.

This turn tests the cheapest version first:

> Does success of the five branchwise rawModSwitch/recryption noise gates imply a nontrivial deterministic upper bound on the nonconstant part presented to the later RM10/joint key switches?

## Primary hypothesis

Conditioned on a fixed successful raw transcript and its HElib recryption-noise bound, the post-reconstruction nonconstant ciphertext part is sufficiently constrained that a small deterministic \`breakIntoDigits\` upper bound can be derived without probabilistic assumptions on the evaluation-key ciphertext.

Falsifier:
show that the recryption-key ciphertext contains fresh independent masking randomness that is not constrained by raw success, and that this randomness directly controls the nonconstant reconstructed part.

## 1. recryptEkey contains an independently randomized second part

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/keys.cpp:1671-1705\`: \`SecKey::genRecryptData\`;
- \`src/keys.cpp:1533-1618\`: secret-key BGV \`Encrypt\`;
- \`src/keys.cpp:33-77\`: \`RLWE\` / \`RLWE1\`;
- \`src/DoubleCRT.cpp:1257-1378\`: \`DoubleCRT::randomize\`.

\`genRecryptData\`:
1. samples the bootstrapping secret \(s_R\);
2. generates the key-switch matrix from key 0 to \(s_R\);
3. encrypts \(s_R\) as \`recryptEkey\` under key 0.

Secret-key \`Encrypt\` constructs a fresh RLWE ciphertext.

In \`RLWE\`:

\[
c_1.\texttt{randomize()}
\]

is executed first, and then

\[
c_0 = p e - c_1 s_0
\]

is formed.

\`DoubleCRT::randomize\` fills every CRT row entry with a uniformly sampled residue modulo that row prime. Its support includes every residue, including zero.

Therefore the nonconstant part

\[
E_1:=\texttt{recryptEkey.parts[1]}
\]

is fresh full-support RLWE masking randomness, sampled independently after the bootstrapping secret and the key-switch matrix have been fixed.

## 2. rawModSwitch success does not inspect E1

The five branchwise candidate prefixes are

\[
\text{S2C}
\to
\text{reLinearize}(s_R)
\to
\text{rawModSwitch}
\to
\text{public carry/divisibility processing}.
\]

The source recryption gate computes its raw-mod-switch noise ratio before assigning

\[
\texttt{ctxt = recryptEkey}.
\]

Thus the event

\[
E_{\rm raw}^c
\]

and the realized public post-raw transcript

\[
(A,B)
\]

do not depend on the fresh RLWE encryption randomness \(E_1\) inside \`recryptEkey\`.

Conditioning on:
- the same secret keys;
- the same key-switch matrices;
- the same input ciphertext;
- the same raw tie tape;
- the same successful raw transcript \((A,B)\);

does not fix \(E_1\).

## 3. Exact reconstructed nonconstant part

The durable handle/reconstruction result gives

\[
\operatorname{Rec}(A,B)
=
(BE_0+fA,\;BE_1).
\]

Hence the nonconstant part entering subsequent automorphism/key-switch work is exactly

\[
\boxed{
C_1 = B E_1.
}
\]

The raw-success condition constrains the secret-linear-form semantics that produced \(A,B\), but it does not constrain \(E_1\).

## 4. Same successful raw transcript can yield different digit norms

Fix any valid successful raw transcript with

\[
B\neq0
\]

as a ring element modulo the active ciphertext modulus.

Multiplication by \(B\) is then a nonzero endomorphism of the finite ciphertext ring, so there exists at least one \(\Delta\) such that

\[
B\Delta\neq0.
\]

Because \`DoubleCRT::randomize\` has full residue support, both

\[
E_1=0
\]

and

\[
E_1=\Delta
\]

are valid support points of the source RLWE masking distribution.

They leave the entire pre-reconstruction raw transcript unchanged.

But after reconstruction:

\[
C_1^{(0)}=0,
\qquad
C_1^{(1)}=B\Delta\neq0.
\]

Since \`breakIntoDigits\` is an exact decomposition of the actual DoubleCRT part:

\[
D(C_1^{(0)})=0,
\]

while

\[
D(C_1^{(1)})>0.
\]

Thus even after fixing the full successful raw transcript \((A,B)\),

\[
\boxed{
D(C_1)
\text{ is not determined by raw success or raw decryption-noise bounds.}
}
\]

This is stronger than Turn 8's generic same-\`noiseBound\` witness: it applies at the exact current candidate reconstruction boundary.

## 5. Why this kills Route C

A theorem of the form

\[
E_{\rm raw}^c
\Longrightarrow
D(C_1)\le F(\text{raw noise bound})
\]

cannot produce a nontrivial source-independent bound unless \(F\) also covers the independent full-support randomness in \(E_1\).

The only universally valid bound derived without distributional assumptions must therefore range over the support of \(BE_1\), i.e. a worst-case ciphertext-part bound.

Raw success alone gives no reason for that worst case to be small relative to the key-switch digit moduli.

Hence:

\[
\boxed{
\text{raw-success envelope}
\not\Rightarrow
\text{small deterministic post-reconstruction digit norm}.
}
\]

Route C is killed.

## 6. HElib's own uniform-digit bound is explicitly probabilistic

Pinned \`DoubleCRT::breakIntoDigits\` contains an older/commented alternative that would estimate each digit using

\[
\texttt{noiseBoundForUniform}
\left(
\frac{Q_{\rm digit}}{2},
\phi(m)
\right).
\]

Pinned \`Context.h\` explicitly labels these routines:

> high probability bounds

and states that \`noiseBoundForUniform\`:
- assumes coefficients are independently uniform;
- uses a normal approximation;
- is "a bit heuristic";
- returns a bound exceeded with probability at most a selected \(\epsilon\).

Therefore HElib itself does not treat this as a deterministic consequence of decryption noise.

The useful small digit-norm bound is distributional.

## 7. Consequence for Route A

Turn 8's Route A is not completely impossible, but its meaning changes.

A useful bound on candidate RM10/joint digit norms must exploit additional state/distribution such as:
- the full public multiplier \(B\);
- the distribution of \(E_1\);
- the distribution induced by prior automorphism/key-switch steps;
- correlations created by repeated use of the same \(j=1\) matrix.

It cannot be derived solely from:
- rawModSwitch success;
- the scalar decryption \`noiseBound\`;
- final capacity.

In particular, if one uses HElib's uniform-digit model, the resulting argument is a **high-probability / key-averaged analysis**, not a deterministic domination proof.

## 8. DFR strategy after this gate

The deterministic DFR-transfer portfolio is now:

### Killed / parked
- actual-error pointwise domination by Corr./TnM;
- scalar-\`noiseBound\` closed recurrence;
- raw-success-to-small-digit deterministic bound.

### Still possible
- a source-specific high-probability analysis of the candidate's digit norms;
- a distributional comparison against Corr./TnM;
- runtime digit-norm traces as artifact evidence;
- a stronger full-state theorem exploiting additional algebraic restrictions beyond raw success, if such restrictions are later discovered.

The first two require genuine probabilistic modeling and are not justified before systems value is known.

## 9. Interaction with the pending native task

The pending paired benchmark remains the correct current priority.

If it FAILS the systems-value gate:
- stop DFR work on this candidate.

If it STRONG-PASSES:
- do not return to deterministic scalar/raw-success domination;
- next analyze the distribution of \`breakIntoDigits\` along RM10/joint recovery, explicitly separating:
  - randomness in \`recryptEkey\`;
  - fixed evaluation-key matrix errors;
  - fresh input ciphertext randomness;
  - repeated-use correlations.

This should be an analytical/probabilistic gate before any large Monte Carlo task.

## Verdict

\`\`\`text
RESULT:
  FAIL_RAW_SUCCESS_TO_DETERMINISTIC_DIGIT_BOUND

RECRYPTEKEY_E1:
  FRESH FULL-SUPPORT RLWE MASKING RANDOMNESS

RAW_SUCCESS_DEPENDS_ON_E1:
  NO

POST_RECONSTRUCTION_NONCONSTANT_PART:
  C1 = B * E1

FIXED_RAW_TRANSCRIPT_DETERMINES_DIGIT_NORM:
  NO

SOURCE_WITNESS:
  E1=0 versus E1=Delta with B*Delta != 0
  SAME RAW TRANSCRIPT / DIFFERENT breakIntoDigits NORM

HELIB noiseBoundForUniform:
  HIGH-PROBABILITY / HEURISTIC
  NOT DETERMINISTIC

ROUTE_C_DIRECT_RAW-SUCCESS BOUND:
  KILLED

ROUTE_A_ANALYTIC_DIGIT BOUND:
  ONLY PLAUSIBLE WITH DISTRIBUTIONAL/FULL-STATE INPUT
  NO LONGER A PURE DETERMINISTIC TRANSFER ROUTE

DFR_AFTER_SYSTEMS_PASS:
  PROBABILISTIC / KEY-AVERAGED ANALYSIS REQUIRED UNLESS NEW STRUCTURE FOUND

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The current candidate's DFR uncertainty is not caused by the fusion/carry semantics; those are pathwise exact.

It is caused by the fact that after exact reconstruction, later key switches act on ciphertext parts containing independent RLWE masking randomness that the raw-success event never constrained.

Therefore the next DFR theory, if the systems benchmark justifies it, must be probabilistic rather than a deterministic corollary of the existing recryption noise gate.
