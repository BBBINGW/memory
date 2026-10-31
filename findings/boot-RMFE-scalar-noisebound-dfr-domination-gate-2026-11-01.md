# BOOT RMFE Scalar-noiseBound DFR-Domination Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 8/25
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

\`BBBINGW/memory main@bde687eb0f270be96fa134ea9e786698109c8b0a\`.

Turn 7 killed actual-error pointwise domination but left open one deterministic DFR route:

> compare the candidate and Corr./TnM using HElib's conservative \`noiseBound\` ledger rather than realized evaluation-key errors.

This turn tests the cheapest version of that route:

> Is HElib's scalar BGV state \((\texttt{noiseBound},\texttt{primeSet},\texttt{ptxtSpace},\texttt{intFactor})\), together with the already-known operation counts and public multiplier norms, sufficient to derive a universal post-raw candidate-vs-baseline ledger domination theorem?

## Primary hypothesis

The scalar HElib bookkeeping state is closed under key switching strongly enough that one can compare the two recovery schedules without knowing the actual ciphertext-part digit decompositions.

Falsifier:
show that two valid ciphertexts can have the same scalar bookkeeping state but different \`breakIntoDigits\` norms, so the next key-switch ledger increment is not determined by that scalar state.

## 1. Same-context Frobenius matrices have the same stored key-switch noise bound

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/keys.cpp:33-64\`: \`RLWE1\`;
- \`src/keys.cpp:1152-1238\`: \`GenKeySWmatrix\`;
- \`src/sample.cpp:445-532\`: \`sampleGaussianBounded\`.

For one fixed bootstrappable BGV context, every direct automorphism matrix used here has the same:
- target secret distribution;
- Gaussian stdev;
- plaintext-space parameter selected by \`GenKeySWmatrix\`;
- cyclotomic dimension.

\`sampleGaussianBounded\` returns the deterministic bound

\[
B_{\rm G}
=
\sigma\cdot \texttt{sampleGaussianBoundedEffectiveBound(context)}
\]

after rejection-sampling until the sampled error lies inside that bound.

\`RLWE1\` then multiplies the returned bound by the common BGV key-switch plaintext-space factor.

Therefore every same-context direct Frobenius key-switch matrix in the current BSGS+10 keyset has the same recorded scalar bound

\[
\boxed{
W.\texttt{noiseBound}=\beta_{\rm KS}
}
\]

independent of its automorphism target.

Thus target identity does not explain ledger differences.

## 2. The next KS ledger increment depends on actual digit norms, not only current noiseBound

Pinned source:
- \`src/Ctxt.cpp:805-842\`: \`keySwitchPart\`;
- \`src/DoubleCRT.cpp:477-560\`: \`breakIntoDigits\`.

For a key-switched source part \(c\),

\[
\Delta \nu_{\rm KS}
=
\texttt{breakIntoDigits}(c)\cdot \beta_{\rm KS}.
\]

But \`breakIntoDigits\` does not return a function of \`ctxt.noiseBound\`.

It:
1. decomposes the actual DoubleCRT part into context digits;
2. CRT-lifts each digit back to a polynomial;
3. computes the actual
   \[
   \texttt{embeddingLargestCoeff(poly)}
   \]
   for every digit;
4. returns the sum of those exact digit embedding norms.

Therefore two ciphertexts with identical scalar \`noiseBound\` can incur different next-step KS ledger increments.

## 3. Source witness: fresh encryptions have fixed scalar noise bounds but random parts

Pinned \`PubKey::Encrypt\`:
- multiplies the public-key ciphertext by a fresh random small polynomial \(r\);
- adds fresh bounded Gaussian error polynomials \(e_0,e_1\);
- therefore the actual ciphertext parts vary from encryption to encryption.

For ordinary BGV encryption (\`highNoise=false\`):
- \`sampleSmallBounded\` returns a context/Hamming-weight-dependent fixed bound after rejection sampling;
- \`sampleGaussianBounded\` returns a context/stdev-dependent fixed bound after rejection sampling;
- the plaintext contribution uses the same deterministic \`ptxt_bound\`.

Hence for the same context and same plaintext, fresh encryption randomness changes the actual ciphertext parts while the source constructs the same scalar bookkeeping formula

\[
\nu_{\rm enc}
=
B_r\nu_{\rm pk}
+
pB_{e_0}
+
pB_{e_1}B_s
+
B_{\rm ptxt}.
\]

So source-faithful ciphertexts exist with:

\[
\boxed{
\text{same }(\texttt{noiseBound},\texttt{primeSet},\texttt{ptxtSpace},\texttt{intFactor})
\quad\text{but different ciphertext parts}.
}
\]

Since their parts differ, their exact \`breakIntoDigits\` norms can differ.

This is not an artificial metadata mutation; it arises from ordinary source encryption randomness.

## 4. Scalar bookkeeping is therefore not a closed KS state

There is no exact recurrence

\[
\nu_{t+1}=F(\nu_t,\text{context},\text{automorphism target})
\]

for HElib key switching.

The actual recurrence is

\[
\boxed{
\nu_{t+1}
=
\nu_t^{\rm relinearize/modup}
+
\beta_{\rm KS}\,D(c_t),
}
\]

where

\[
D(c_t)=\texttt{breakIntoDigits}(c_t)
\]

is an additional full ciphertext-part state variable.

Automorphism itself preserves \`noiseBound\`, but after each relinearization/addition the next nonconstant part changes, so later \(D(c_t)\) values are path-dependent.

This applies directly to:
- the ten RM10 direct key switches;
- the four chained \(j=1\) recovery key switches;
- the stock Corr./TnM trace/C2S key switches.

Therefore:
- 14 versus 95 physical KS calls is not enough to prove a ledger ordering;
- current/final capacity alone is not enough to reconstruct the intermediate KS ledger;
- known public-multiplier norms alone do not close the comparison.

## 5. Public multipliers are closed scalar operations; KS is the obstruction

Pinned BGV \`multByConstant(ZZX)\` computes

\[
\nu\leftarrow \nu\cdot
\|\theta\|_{\rm can}
\]

using \`embeddingLargestCoeff\`.

So public-multiplier propagation *is* scalar-bookkeeping closed once the multiplier norm is known.

The current joint map has already-audited multiplier sums and worst direct tax:

\[
15.740880\text{ bits}.
\]

Likewise the RM10 unit normalization \(224\) has zero direct \`noiseBound\` multiplication under the scalar-unit overload.

Thus the unresolved state dependence is specifically the key-switch digit norm sequence, not the already-known public multiplier ledger.

## 6. Why the old reconstruction dominance result still stands

This turn does not disturb the durable one-reconstruction result.

At the reconstruction boundary, the fused ciphertext satisfies

\[
\nu_{\rm fused}\le \nu_{\rm separate-sum}
\]

because both schedules reuse the same \`recryptEkey\` and the public aggregate multipliers obey the embedding triangle inequality.

The non-closure appears **afterward**, when the candidate and baseline feed different actual ciphertext parts into different automorphism/relinearization schedules.

Therefore:

\[
\boxed{
\text{reconstruction ledger dominance PASS}
\not\Rightarrow
\text{whole recovery ledger dominance}.
}
\]

## 7. Consequence for DFR-transfer strategy

The cheapest deterministic DFR-transfer route from Turn 7 is therefore killed in its scalar-only form.

One cannot prove

\[
\nu_{\rm cand}^{\rm post}
\le
\nu_{\rm prior}^{\rm post}
\]

for all source-faithful inputs using only:
- starting \`noiseBound\`;
- physical KS counts;
- key-switch target identities;
- public multiplier norms.

A valid deterministic proof would need one of the following additional ingredients:

### Route A — full-state analytic digit bound

Prove an explicit source-shaped bound on

\[
D(c_t)=\texttt{breakIntoDigits}(c_t)
\]

at every candidate and comparator KS state, derived from the ring/modulus structure rather than measured values.

### Route B — exact runtime digit trace as evidence, not theorem

Instrument and record every \`breakIntoDigits\` norm and resulting \`noiseBound\` transition.

This can validate a particular native artifact but does not by itself establish negligible DFR over all keys/inputs.

### Route C — direct candidate correctness bound

Forget baseline domination and prove the candidate's own post-raw ledger stays below the HElib correctness threshold for every state admitted by the rawModSwitch success conditions.

This would require a new relation from the raw-success envelope to later digit norms; no such relation is currently established.

## 8. Interaction with the pending native task

The pending paired benchmark remains valid for:
- latency;
- throughput;
- final capacity;
- correctness smoke testing;
- physical-hop audit.

Its final capacity result is valuable systems evidence.

But unless its artifact already records internal digit norms, it cannot retroactively supply a universal DFR proof.

Do not modify or rerun it.

If the pending task is a systems FAIL, no further DFR work is justified.

If it is a STRONG systems PASS, the next DFR step should first inspect whether a cheap analytic bound on \`breakIntoDigits\` can be made non-vacuous for the exact RM10/joint states before considering any new native instrumentation.

## Verdict

\`\`\`text
RESULT:
  FAIL_SCALAR_NOISEBOUND_CLOSED_DOMINATION

SAME_CONTEXT_FROBENIUS_W_NOISEBOUND:
  SAME DETERMINISTIC BOUND beta_KS

KS_LEDGER_INCREMENT:
  beta_KS * exact breakIntoDigits(part)

BREAKINTODIGITS_DEPENDS_ON:
  ACTUAL CIPHERTEXT PARTS
  NOT SCALAR noiseBound ALONE

SAME_SCALAR_STATE_DIFFERENT_DIGIT_NORMS:
  SOURCE-POSSIBLE VIA FRESH BGV ENCRYPTION RANDOMNESS

PHYSICAL_KS_COUNT_ONLY_DFR_TRANSFER:
  INVALID

PUBLIC_MULTIPLIER_LEDGER:
  SCALAR-CLOSED / ALREADY AUDITED

RECONSTRUCTION_LEDGER_DOMINANCE:
  PRESERVED LOCALLY

WHOLE_RECOVERY_NOISEBOUND_DOMINATION:
  NOT ESTABLISHED

CHEAP_SCALAR-ONLY DFR ROUTE:
  KILLED / PARK

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The DFR problem is now localized more sharply.

The obstruction is not target-specific key-switch noise bounds: those are uniform across the direct Frobenius matrices.

The obstruction is that HElib's key-switch ledger needs the actual digit decomposition norms of the current ciphertext part, and those are not encoded by the scalar capacity/noiseBound state.

Therefore no further turn should try to infer DFR merely from 95->14 KS counts or from final capacity.

Only if the pending systems gate is strong should BOOT spend effort on a source-shaped analytic digit-norm bound or, if necessary, later exact digit-trace instrumentation.
