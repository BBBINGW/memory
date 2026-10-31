# BOOT RMFE intFactor / Downstream Semantics Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 16/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn tests one independent correctness condition:

> Does the carry-compensated single reconstruction plus RM10 normalization plus joint correction recovery preserve HElib's BGV \`ptxtSpace/intFactor\` semantics so that downstream correction DigitExtract remains well-typed and plaintext-equivalent to the five-branch baseline?

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Pinned HElib invariant

Pinned HElib source uses the BGV invariant

\[
[\langle sk,ct\rangle]_Q
=
\texttt{intFactor}\cdot Q\cdot m
\pmod{\texttt{ptxtSpace}}.
\]

Decryption explicitly divides by

\[
\texttt{intFactor}\cdot Q
\]

modulo the ciphertext plaintext space.

Thus \`intFactor\` is an invertible plaintext scaling metadata value, not a requirement that the internal factor equal 1.

## Stock thinReCrypt behavior

At entry, stock \`PubKey::thinReCrypt\` saves

\[
f_{\rm in}=\texttt{ctxt.intFactor}.
\]

After branch-local slotToCoeff / relinearization / rawModSwitch / divisibility lift, it executes

\[
\texttt{ctxt = recryptEkey}.
\]

The source explicitly comments:

\`here we lose the intFactor associated with ctxt. We will restore it below.\`

The bootstrapping key ciphertext is created by \`SecKey::genRecryptData\` via \`Encrypt\`, and HElib encryption initializes

\[
\texttt{intFactor}=1.
\]

At the very end of \`thinReCrypt\`, after \`extractDigitsThin\` has reduced the plaintext space back to the application plaintext space, stock HElib restores the saved factor multiplicatively:

\[
\texttt{ctxt.intFactor}
\leftarrow
\texttt{ctxt.intFactor}\cdot f_{\rm in}
\bmod \texttt{ptxtSpace}.
\]

It does **not** overwrite the internal factor with \(f_{\rm in}\).

This distinction matters for the revised candidate.

## Single reconstruction preserves the same temporary state

The revised candidate combines the two public post-rounding parts into

\[
A=\sum_iY^i a_i,\qquad
B=\sum_iY^i b_i
\]

and reconstructs once:

\[
C=A+B K,
\]

where \(K\) is the same \`recryptEkey\`.

The reconstruction uses exactly the same HElib pattern:

\[
\texttt{ctxt = recryptEkey};
\quad
\texttt{ctxt.multByConstant}(B);
\quad
\texttt{ctxt.addConstant}(A).
\]

For BGV:

- polynomial \`multByConstant\` does not change \`intFactor\`;
- \`addConstant\` scales the injected constant according to the current \`intFactor\` and prime product;
- the reconstructed ciphertext therefore remains a valid HElib ciphertext in the same temporary plaintext-space semantics as stock recryption.

The public carry corrections from Turns 11–12 occur before encrypted reconstruction and introduce no separate ciphertext metadata state.

## RM10 normalization changes metadata but is semantically valid

The exact RM10 path requires one scalar normalization

\[
224=(2^{10})^{-1}\pmod{625},
\]

with inverse

\[
224^{-1}=399\pmod{625}.
\]

HElib's BGV scalar overload \`multByConstant(const ZZ& c)\` computes

\[
d=\gcd(c,\texttt{ptxtSpace}).
\]

For a unit \(c\), it updates

\[
\texttt{intFactor}
\leftarrow
\texttt{intFactor}\cdot c^{-1}
\pmod{\texttt{ptxtSpace}}
\]

and returns without multiplying ciphertext parts or \`noiseBound\`.

Hence, when the current temporary plaintext space is the established ring

\[
S=\mathbb Z/625\mathbb Z,
\]

the required normalization

\[
\times224
\]

changes

\[
\texttt{intFactor}:1\to399
\]

while preserving the exact BGV invariant.

This is not an error and is not a plaintext mismatch.

It is precisely HElib's unit-scalar representation of multiplying the semantic plaintext by 224.

## Joint recovery preserves one common factor

The four-output joint recovery is built from:

- copies of one ciphertext;
- Frobenius / smart automorphisms;
- polynomial plaintext multiplications;
- ciphertext additions.

Pinned HElib behavior:

- Frobenius/automorphism preserves \`intFactor\`;
- hoisted automorphism explicitly initializes every result with the source ciphertext's \`intFactor\`;
- polynomial \`multByConstant\` preserves \`intFactor\`;
- addition only invokes factor harmonization if the two inputs have different factors.

All four correction outputs originate from the same normalized ciphertext.

Therefore they all carry the **same**

\[
\texttt{intFactor}=399
\]

at the output of the joint linear map, modulo any later generic arithmetic changes.

No factor-harmonization is required merely to combine the four joint-map outputs.

## Downstream DigitExtract supports arbitrary unit factors

HElib's ciphertext arithmetic is designed around the modified BGV invariant and is valid for arbitrary invertible \`intFactor\`.

Relevant downstream operations preserve the semantic plaintext while updating metadata:

- ciphertext multiplication updates \`intFactor\` according to the BGV invariant;
- addition harmonizes two differing unit factors before adding;
- \`divideByP\` divides the plaintext space by \(p\) and reduces
  \[
  \texttt{intFactor}\bmod\texttt{newPtxtSpace};
  \]
- \`multByP\` changes plaintext space and invokes the scalar-multiplication metadata logic;
- \`reducePtxtSpace\` reduces both plaintext space and \`intFactor\` modulo the new space.

Therefore correction DigitExtract is not semantically restricted to \`intFactor=1\`.

A unit factor such as

\[
399\pmod{625}
\]

may safely flow through the correction/DigitExtract circuit.

After reduction to the application plaintext space \(p=5\),

\[
399\bmod5=4,
\]

which is still a unit.

## Correct final restoration rule

Let \(f_{\rm in}\) be the original application-ciphertext factor saved before splitting.

The revised implementation must **not** do

\[
\texttt{ctxt.intFactor}=f_{\rm in}.
\]

It must follow the stock HElib rule:

\[
\boxed{
\texttt{ctxt.intFactor}
\leftarrow
\texttt{ctxt.intFactor}\cdot f_{\rm in}
\bmod p^r.
}
\]

Reason:

the temporary bootstrap computation has intentionally discarded the original metadata while the underlying branch values still carry the corresponding semantic scale.

Multiplying the final internal factor by \(f_{\rm in}\) removes that original scale at decryption exactly as stock \`thinReCrypt\` does.

The internal factor need not equal 1 before restoration.

Thus RM10's temporary factor 399 requires **no special inverse compensation** at the final boundary.

## Plaintext-space type condition

The exact joint Moore coefficients from Turns 7–8 were constructed over

\[
S=\mathbb Z/625\mathbb Z.
\]

Therefore the implementation must assert, at the reconstruction / joint-map boundary, that the temporary bootstrapping ciphertext plaintext space is exactly the established \(625\)-ring interface.

Required runtime/static contract:

\[
\boxed{
\texttt{joint-map ptxtSpace}=625.
}
\]

If the actual \`recryptEkey\` plaintext space in the source-faithful p=5 instance is not 625, the stored \(\theta_{t,j}\) are ill-typed and the candidate must stop rather than silently reducing/lifting them.

This is an implementation/type assertion, not a new native experiment.

The existing deterministic RMFE/R8 findings already use the 625 interface; the candidate implementation must preserve that same source lineage.

## Capacity side note

Although correctness is preserved for arbitrary unit \`intFactor\`, the exact value of the factor can affect HElib's noise bookkeeping when two ciphertexts with different factors are added, because \`addCtxt\` may multiply by unit harmonization coefficients.

The four direct correction outputs themselves share one factor and do not trigger this issue.

Whether later nonlinear correction-DigitExtract intermediates incur factor-harmonization noise different from the baseline remains a capacity question, not a correctness blocker.

No capacity equivalence is claimed here.

## Verdict

\`\`\`text
RESULT:
  PASS_STATIC_INTFACTOR_DOWNSTREAM_SEMANTICS

SINGLE_RECONSTRUCTION_TEMP_INTFACTOR:
  VALID / inherited from recryptEkey

RM10_NORMALIZATION_224:
  intFactor 1 -> 399 mod 625
  SEMANTICALLY VALID
  ZERO DIRECT noiseBound MULTIPLICATION

JOINT_RECOVERY_FACTOR:
  COMMON ACROSS ALL FOUR OUTPUTS

DIGITEXTRACT_REQUIRES_INTFACTOR_ONE:
  NO

FINAL_RESTORE_RULE:
  current_intFactor *= saved_input_intFactor mod application ptxtSpace

SPECIAL_399_COMPENSATION_AT_END:
  NOT REQUIRED

JOINT_MAP_PTXTSPACE_TYPE_ASSERT:
  REQUIRED: 625

PLAINTEXT_CORRECTNESS_BLOCKER:
  NONE FOUND

CAPACITY_EFFECT_OF_LATER_FACTOR_HARMONIZATION:
  UNRESOLVED

NATIVE_CORRECTNESS:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The revised carry-compensated single reconstruction is not killed by HElib \`intFactor\` semantics.

The important implementation rule is to preserve HElib's metadata discipline rather than manually resetting factors.

This gate also clarifies Turn 15:

- normalization by 224 is capacity-free at the direct scalar-multiplication step;
- but it is not metadata-free.

If the pending timer remains unavailable, the next independent static falsifier should target the one remaining correctness boundary not covered by this gate:

> whether the post-raw aggregation and carry correction preserve HElib's **two-part secret-key handle / recrypt-key linear form** exactly after branch-specific \`reLinearize(recryptKeyID)\`, including the placement of the monomial \(Y^i\) shifts relative to the encrypted secret-key term.

That is a source-type/secret-handle correctness audit independent of latency.

AI_PROVISIONAL_CHOICE:
  RETAIN_REVISED_POSTRAW_FUSION
  REQUIRE_PTXTSPACE_625_ASSERT
  PRESERVE_STOCK_INTFACTOR_RESTORE_DISCIPLINE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
