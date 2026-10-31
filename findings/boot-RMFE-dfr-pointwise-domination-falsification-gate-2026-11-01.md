# BOOT RMFE Post-Raw DFR Pointwise-Domination Falsification Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 7/25
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

\`BBBINGW/memory main@d253ed852ca6127472b7ab9a635854b0b03d6f21\`.

Turn 6 left one highest-value DFR reopening route:

> condition on successful branchwise rawModSwitch and try to prove that the candidate post-raw error/noise is pointwise dominated by the stock Corr./TnM path, so baseline DFR transfers without empirical negligible-probability estimation.

This turn tests that route only.

## Primary hypothesis

Under the identical BSGS+10 evaluation-key set from the paired benchmark contract, for every valid keyset and source-faithful post-raw state, the candidate's actual post-raw decryption error is pointwise no larger than the stock Corr./TnM comparator's error.

Falsifier:

- identify a valid evaluation-key error direction that affects the candidate but is not read by the comparator;
- show that key switching injects that error with a nonzero digit coefficient for some valid state.

If such a direction exists, no universal actual-error domination theorem can hold.

## 1. Exact key-switch error dependence

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/keys.cpp:33-64\`: \`RLWE1\`;
- \`src/keys.cpp:1152-1238\`: \`GenKeySWmatrix\`;
- \`src/Ctxt.cpp:191-230\`: \`keySwitchDigits\`;
- \`src/Ctxt.cpp:805-842\`: \`keySwitchPart\`;
- \`src/DoubleCRT.cpp:477-560\`: \`breakIntoDigits\`;
- \`src/sample.cpp:175-200,459-532\`: rounded Gaussian sampling and bounded rejection.

For one key-switch matrix \(W\), write its digit rows as \((a_j,b_j)\).
Source generation gives, under the target secret \(s\),

\[
b_j+a_js
=
P_j s' + p e_j,
\]

where:
- \(s'\) is the source secret/automorphed secret represented by \`fromKey\`;
- \(P_j\) is the digit basis factor;
- \(e_j\) is the short RLWE error polynomial sampled for row \(j\).

If the source ciphertext part \(c\) is decomposed by \`breakIntoDigits\` as digits \(d_j\), then \`keySwitchDigits\` adds

\[
d_j a_j
\]

to the target-secret part and

\[
d_j b_j
\]

to the constant part.

Decrypting the switched contribution therefore gives the desired source-secret term plus

\[
\boxed{
p\sum_j d_j e_j
}
\]

as the actual key-switch error contribution.

Thus the candidate output depends linearly and nontrivially on a matrix's sampled \(e_j\)'s whenever at least one digit \(d_j\) is nonzero.

For any nonzero source ciphertext part, \`breakIntoDigits\` cannot return all-zero digits, because the digit decomposition reconstructs that part over its active CRT primes.

## 2. Equal-keyset BSGS+10 exact baseline paths

Use Frobenius exponent-index notation:

\[
\sigma_j : X\mapsto X^{5^j}.
\]

Standard BSGS direct exponent edges are:
- babies \(1,\ldots,90\);
- giants \(91,182,\ldots,8190\).

The ten appended direct RM10 exponent indices are

\[
\{4096,6144,7168,7680,7936,3968,6080,5088,2032,888\}.
\]

HElib \`setKeySwitchMap\` performs FIFO BFS and scans direct matrices in insertion order.
Under the paired contract, standard BSGS matrices are generated first and the ten RM10 matrices are appended afterward.

Exact BFS paths for the stock Corr./TnM binary trace targets are:

| trace target \(j\) | exact direct-edge path |
|---:|---|
| 1 | [1] |
| 2 | [2] |
| 4 | [4] |
| 8 | [8] |
| 16 | [16] |
| 32 | [32] |
| 64 | [64] |
| 128 | [37, 91] |
| 256 | [74, 182] |
| 512 | [57, 455] |
| 1024 | [23, 1001] |
| 2048 | [16, 2032] |
| 4096 | [4096] |

The ordinary order-2 slot-dimension generator lies outside the Frobenius subgroup.
A single use leaves the subgroup, while two uses cancel the quotient component, so it cannot shorten any of these one/two-hop subgroup paths.

Consequences:

1. the prior durable equal-keyset physical count remains correct:
   - 18 trace KS per branch;
   - +1 ordinary D=2 KS;
   - 19 per branch;
   - 95 across five branches.

2. the attribution is refined:
   - added RM10 matrix \(e=4096\) is used directly by the baseline;
   - added RM10 matrix \(e=2032\) is also used by the baseline, as the second edge of the 2048 trace path.

Thus the ten RM10 matrices are not all candidate-only under the equal-keyset comparator.

## 3. Eight candidate-only evaluation-key error directions remain

The current candidate uses all ten direct RM10 matrices, plus the direct \(j=1\) matrix for the four-call joint chain.

The stock Corr./TnM trace paths above use only two of the ten added RM10 matrices.

Therefore the following eight RM10 direct matrices are candidate-only for the compared post-raw recovery:

\[
\boxed{
\{888,3968,5088,6080,6144,7168,7680,7936\}.
}
\]

Their corresponding RLWE error polynomials affect the candidate path but do not enter the stock Corr./TnM trace path.

This is a structural dependency difference, not merely a physical-KS count difference.

## 4. Why universal actual-error pointwise domination fails

Fix one of the eight candidate-only matrices \(W^\star\).

For a valid nonzero ciphertext state reaching that RM10 automorphism:
- automorphism is invertible, so a nonzero nonconstant ciphertext part remains nonzero;
- its digit decomposition therefore contains at least one nonzero digit \(d_j\);
- the switched error contains
  \[
  p\,d_j e_j^\star
  \]
  for some row.

The stock Corr./TnM comparator does not read \(W^\star\), so its output is independent of \(e_j^\star\).

HElib's rounded-Gaussian sampler has both zero and nonzero small integer polynomials in its accepted support, and \`sampleGaussianBounded\` accepts any realization whose embedding norm is below the fixed bound.

Therefore the source distribution permits valid key matrices with different accepted \(e_j^\star\) while all comparator-used matrix errors are held fixed.

At the algebraic level, changing \(e_j^\star\) changes candidate actual error but leaves comparator actual error unchanged.

The later candidate operations are not the zero map on the entire ciphertext-error space:
- RM10 continues by ring-linear automorphism/addition operations;
- the joint recovery is a nonzero exact linear map on its active domain.

Hence there exist valid error directions whose effect survives to at least one candidate pre-DigitExtract output.

Consequently there is no universal theorem of the form

\[
\boxed{
\|e_{\rm cand}(K,X)\|
\le
\|e_{\rm prior}(K,X)\|
\quad
\text{for all valid }K,X
}
\]

based on exact sampled errors.

Equivalently, the strongest possible coupled statement

\[
\operatorname{Success}_{\rm prior}(K,X)
\Longrightarrow
\operatorname{Success}_{\rm cand}(K,X)
\]

cannot be obtained merely from an exact-error pointwise domination argument.

This falsifies the Turn-6 proposed *actual-error coupling* route.

## 5. What this does NOT falsify

This result does **not** show the candidate has worse DFR.

It does not even show larger expected error.

The candidate has far fewer physical KS calls under BSGS+10:

\[
95\to14
\]

on the recovery side.

The result only says that the two schedules depend on different fixed evaluation-key error coordinates, so one output's realized error cannot uniformly dominate the other's over every keyset.

In particular, it does not rule out:

1. a deterministic **HElib noiseBound / worst-case-bound domination** theorem;
2. a probabilistic comparison using the joint distribution of matrix errors;
3. a direct analytical DFR proof for the candidate.

## 6. Important distinction: actual error vs HElib noiseBound ledger

For same-context key-switch matrices, HElib stores a common-style high-probability/rejection-enforced bound in \`W.noiseBound\`.

At evaluation, \`keySwitchPart\` adds

\[
\texttt{breakIntoDigits(part)}\times W.\texttt{noiseBound}
\]

to the ciphertext's bookkeeping bound.

This ledger does not expose the realized sign/direction of \(e_j\).

Therefore the failure of actual-error pointwise domination does **not** imply failure of a noiseBound-ledger comparison.

A ledger domination proof would need to compare the full deterministic recurrence:
- digit norms at every candidate RM10/joint KS;
- public multiplier amplification;
- mod-down behavior;
- the corresponding stock trace/C2S recurrence.

That remains open and is the only sensible deterministic DFR-transfer route.

## 7. Implication for the pending paired benchmark

The same-keyset paired benchmark remains scientifically correct for:
- latency;
- capacity;
- correctness smoke testing;
- throughput.

The refined baseline path expectation is:

\[
\boxed{
\text{Corr./TnM recovery under BSGS+10} = 95\text{ physical KS}
}
\]

with baseline use of added RM matrices \(2032\) and \(4096\).

If its artifact reports a different trace-hop structure, that is a provenance/execution issue to audit.

For DFR, however, same-key pairing does not remove all key uncertainty because eight evaluation-key error directions are candidate-specific.

## Verdict

\`\`\`text
RESULT:
  FAIL_UNIVERSAL_ACTUAL_ERROR_POINTWISE_DOMINATION
  PASS_EXACT_EQUAL_KEYSET_BFS_REFINEMENT

BASELINE_BSGS_PLUS10_RECOVERY_KS:
  95
  UNCHANGED

ADDED_RM10_MATRICES_USED_BY_BASELINE:
  e=4096
  e=2032

CANDIDATE_ONLY_RM10_ERROR_DIRECTIONS:
  8
  {888,3968,5088,6080,6144,7168,7680,7936}

KEYSWITCH_ACTUAL_ERROR_TERM:
  p * sum_j digit_j * e_j

BASELINE_DFR_TRANSFER_BY_EXACT_ERROR_COUPLING:
  KILLED

HELIB_NOISEBOUND_DOMINATION:
  STILL OPEN

CANDIDATE_DFR:
  NOT SHOWN WORSE
  NOT SHOWN EQUAL
  NOT SHOWN BETTER

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Turn 6's DFR reopening route must be narrowed.

Do not seek a pathwise theorem comparing realized candidate error to realized Corr./TnM error under one keyset: the two paths read different evaluation-key error coordinates.

If the pending systems gate is strong, the next deterministic DFR attempt should compare HElib's conservative noiseBound recurrences rather than exact sampled errors.

If that ledger comparison also fails to dominate, then key-averaged probabilistic analysis is unavoidable.
