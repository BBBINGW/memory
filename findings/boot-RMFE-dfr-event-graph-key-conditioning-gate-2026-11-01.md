# BOOT RMFE DFR Event-Graph / Key-Conditioning Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 6/25
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

\`BBBINGW/memory main@b12eeef0ad16e704f53e7e5f3593fc6f625c31dd\`.

Relevant durable prerequisites:
- Turn 5 maximal-fusion theorem gate;
- exact recrypt-key handle / single-reconstruction equality;
- fused reconstruction noise/intFactor bookkeeping dominance;
- current paired same-machine native-gate contract.

## Primary hypothesis

Can the current candidate inherit the baseline DFR essentially for free because it preserves branchwise rawModSwitch and only changes deterministic post-raw processing?

Falsifier:
identify candidate-specific stochastic or key-level failure sources, or show that the baseline-success event does not imply candidate success after the fusion boundary.

## 1. Randomness variables must be separated

For one bootstrap invocation define the sampled state as:

- \(K\): secret key, recryption key, public/evaluation keys, including every key-switch matrix;
- \(X\): fresh input-ciphertext randomness and the resulting pre-bootstrap ciphertext state;
- \(\tau\): runtime tie-breaking randomness used by symmetric representative selection.

Conditioned on \((K,X,\tau)\), the entire candidate computation is deterministic.

The global candidate failure probability is therefore

\[
P_{\rm fail}^{\rm cand}
=
\Pr_{K,X,\tau}
[
\operatorname{Fail}_{\rm cand}(K,X,\tau)
].
\]

A benchmark that fixes one generated keyset and repeats fresh ciphertexts estimates at best a conditional quantity

\[
p_K
=
\Pr_{X,\tau}
[
\operatorname{Fail}_{\rm cand}\mid K
],
\]

not the key-averaged DFR \(E_K[p_K]\).

## 2. Evaluation-key Gaussian errors are sampled at key generation, not per KS call

Pinned HElib source:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/keys.cpp:33-64\`: \`RLWE1\`;
- \`src/keys.cpp:1181-1238\`: \`GenKeySWmatrix\`;
- \`src/sample.cpp:445-532\`: \`sampleGaussianBounded\`;
- \`src/Ctxt.cpp:805-842\`: \`keySwitchPart\`.

For each key-switch matrix, \`RLWE1\` samples the error once during key generation.

Moreover, \`sampleGaussianBounded\` is rejection sampling:
- it computes a deterministic embedding-norm bound;
- it resamples until the actual sampled polynomial satisfies the bound;
- after 1000 unsuccessful trials it throws instead of silently accepting an out-of-bound key.

Thus a successfully generated key-switch matrix already has an actual error polynomial inside its recorded bound.

At evaluation time:
- the random bottom row is regenerated from the matrix's fixed PRG seed;
- \`keySwitchPart\` adds a deterministic \`addedNoise\` ledger term using the stored matrix bound;
- no fresh Gaussian key-switch error is sampled.

Therefore:

\[
\boxed{
\text{one physical KS call is NOT one independent DFR event.}
}
\]

In particular, the four chained \(j=1\) calls reuse the same direct \(j=1\) matrix and the same underlying sampled matrix error.

The ten direct RM10 matrices introduce ten additional **key-generation samples**, not ten fresh random trials on every bootstrap invocation.

## 3. Branchwise rawModSwitch failure family is inherited exactly from the baseline

The current candidate intentionally preserves, for all five branches:

\[
\text{S2C}
\to
\text{reLinearize(recryptKeyID)}
\to
\text{rawModSwitch}.
\]

This prefix is source-identical to the corresponding five branch paths of Aung Corr./TnM before the fusion point.

Let

\[
E_{{\rm raw},i}
\]

denote failure of the source recryption noise condition for branch \(i\), including the raw-mod-switch bound.

Under a coupled execution using the same:
- keyset \(K\);
- branch ciphertexts \(X\);
- rawModSwitch tie tape \(\tau\);

the candidate and prior workflow have exactly the same event

\[
E_{\rm raw}
=
\bigcup_{i=0}^{4} E_{{\rm raw},i}.
\]

No independence between the five events is established or required.

If one only knows a marginal per-branch bound \(\delta_i\), the universally valid statement is the union bound

\[
\Pr[E_{\rm raw}]
\le
\sum_i\delta_i,
\]

not a product/independence formula.

This current candidate therefore differs from the old one-core R24 architecture: it has **five preserved branchwise rawModSwitch events**, not one shared raw core event.

Do not import the old "one core failure event" DFR claim into this branch.

## 4. rawModSwitch runtime tie randomness is inherited and pathwise corrected

For odd \(p=5\), the bootstrapping modulus

\[
q=p^e+1
\]

is even.

Pinned \`rawModSwitch\` randomizes between the two centered representatives only at the exact endpoint

\[
x=\pm q/2.
\]

This is the runtime tie tape \(\tau\).

The candidate performs branchwise rawModSwitch before aggregation, so it observes the same realized branch outputs as the stock path under the coupled tape.

Turn 5's post-raw carry formula is pathwise in those realized integer outputs.

Hence the exact carry-compensated fusion remains correct for **every realized tie outcome**.

The fusion introduces no new tie-breaking event.

Pinned \`newMakeDivisible\` only randomizes its half-point when \(p=2\); for current odd \(p=5\) this step is deterministic.

Likewise the current plaintext spaces \(625,125,25,5\) are odd, so the relevant balanced plaintext-space reductions do not introduce the even-modulus half-point randomization used for \(p=2\).

## 5. Single reconstruction introduces no new random source and is pathwise equal to the stock aggregate

Durable Turn 18/19 results establish, for the same realized post-raw branch pairs,

\[
\operatorname{Rec}(A,B)
=
\sum_i Y^i\operatorname{Rec}(a_i,b_i)
\]

at the actual HElib CtxtPart/handle level.

All five stock reconstructions copy the same fixed \`recryptEkey\`.

Therefore fusion does not replace five independent encrypted-key errors by one new sample:
there was only one common \`recryptEkey\` error polynomial to begin with.

The actual common error contribution is

\[
e_E\sum_iY^ib_i
=
e_EB
\]

under both schedules.

The fused HElib noise ledger is also no larger than the separate-sum comparator ledger at this boundary.

Thus there is no reconstruction-specific DFR regression.

## 6. Candidate-specific DFR uncertainty starts at RM10 / joint recovery

After the common reconstruction, the prior and candidate schedules diverge.

Prior Corr./TnM:
- five branch-local inverse transforms / C2S paths;
- recombination;
- correction DigitExtract.

Current candidate:
- RM10;
- unit normalization;
- chained rank-5 joint recovery;
- correction DigitExtract.

The candidate uses the ten added direct RM10 matrices and the direct \(j=1\) matrix.

Those matrices contain fixed, bounded key-generation errors, and the later operations deterministically propagate:
- ciphertext noise from \(X\);
- recrypt-key error;
- key-switch-matrix errors from \(K\).

There is currently no theorem showing

\[
\operatorname{Fail}_{\rm prior}^c
\Longrightarrow
\operatorname{Fail}_{\rm cand}^c
\]

or, equivalently, that candidate post-raw noise is pointwise dominated by the prior workflow.

Therefore baseline DFR does **not** transfer automatically.

Fewer physical key switches also do not prove lower DFR because:
- digit decomposition norms depend on the current ciphertext state;
- public multiplier norms differ;
- the two schedules use different transforms.

The correct status is:

\[
\boxed{
\text{pre-fusion DFR family inherited; post-fusion DFR transfer unresolved.}
}
\]

## 7. Failure-event graph

A useful exact decomposition is

\[
E_{\rm cand}
=
E_{\rm raw}
\cup
E_{\rm post}^{\rm cand},
\]

where \(E_{\rm post}^{\rm cand}\) is candidate failure after all five branch rawModSwitch calls have succeeded.

Hence

\[
\Pr[E_{\rm cand}]
\le
\Pr[E_{\rm raw}]
+
\Pr[E_{\rm post}^{\rm cand}].
\]

The fusion/reconstruction lemma lets the post event be localized more sharply:

\[
E_{\rm post}^{\rm cand}
\]

need not include a separate "fusion randomness" or "recryptEkey fusion" event.

The genuinely candidate-specific region begins at RM10 / joint recovery and continues through correction DigitExtract.

This is the correct target for any later DFR proof.

## 8. Statistical unit for the pending paired native task

One candidate invocation outputs one RMFE-packed result containing ten logical packed values and four joint correction outputs internally.

The whole invocation is ONE Bernoulli correctness trial.

Do not count:
- ten packed logical values as ten independent trials;
- four joint outputs as four independent trials;
- fourteen physical KS calls as fourteen independent DFR events.

The outputs share:
- one keyset;
- one input ciphertext history;
- one fused reconstruction;
- one RM10 chain;
- overlapping key-switch matrices.

Their failure events are strongly coupled.

## 9. What 20 same-key PASS runs can and cannot establish

The pending task uses 20 measured invocations per workflow under one fixed generated keyset unless its artifact explicitly shows otherwise.

Even granting 20 independent invocation-level trials, observing zero failures gives only:

- one-sided 95% binomial upper bound about \(13.91\%\);
- two-sided Clopper-Pearson 95% upper endpoint about \(16.84\%\).

This is a correctness smoke test, not meaningful evidence for a cryptographic DFR such as \(2^{-40}\) or \(2^{-60}\).

Halevi-Shoup's HElib parameter analysis explicitly targets negligible error using high-probability analytical bounds; their default \(k=10\) discussion gives an order-\(2^{-60}\) aggregate target for reasonable \(m\), not something that can be validated by tens of executions.

Therefore:

\[
\boxed{
\text{pending 20-run correctness PASS must not be relabeled as DFR PASS.}
}
\]

## 10. Cheapest reopening condition after a native STRONG PASS

Do not start brute-force multi-million-run DFR testing.

The next DFR step, only if systems value survives, should first seek a **deterministic/noise-bound domination proof** for the candidate-specific post-raw region:

1. condition on successful five-branch rawModSwitch;
2. use actual HElib \`noiseBound\` recurrences for the ten direct RM10 KS and four chained \(j=1\) KS;
3. compare the candidate final pre-DigitExtract noise/capacity condition against the source Corr./TnM comparator;
4. propagate through the six established DigitExtract divide-by-\(p\) boundaries.

If a pointwise domination theorem can be proved, DFR transfer may follow from the source parameter analysis without empirical estimation of negligible probabilities.

If no domination theorem exists, a correct DFR study must randomize at the **keyset level** as well as the invocation level and must report key-conditioned versus key-averaged results separately.

That would be a later dedicated task, not the pending benchmark.

## Verdict

\`\`\`text
RESULT:
  PASS_DFR_EVENT_GRAPH_CLOSED
  FAIL_BASELINE_DFR_AUTOMATIC_TRANSFER

BRANCH_RAWMODSWITCH_EVENTS:
  FIVE
  PATHWISE IDENTICAL TO STOCK CORR/TNM PREFIX

ONECORE_SINGLE_EVENT CLAIM:
  NOT APPLICABLE TO CURRENT CANDIDATE

FUSION_ADDS_RANDOMNESS:
  NO

SINGLE_RECONSTRUCTION_ADDS_RANDOMNESS:
  NO

KEYSWITCH_CALLS_AS_INDEPENDENT_DFR_EVENTS:
  FALSE

DIRECT_RM10_KEY_ERRORS:
  SAMPLED / BOUNDED AT KEYGEN
  FIXED DURING EVALUATION

CHAINED_J1_FOUR_CALLS:
  REUSE SAME J1 MATRIX ERROR SOURCE

CANDIDATE_SPECIFIC_DFR_REGION:
  RM10 + JOINT RECOVERY + DOWNSTREAM DIGITEXTRACT

20_RUN_CORRECTNESS:
  SMOKE TEST ONLY
  NOT DFR EVIDENCE

OUTPUT_TRIAL_UNIT:
  ONE FULL PACKED BOOTSTRAP INVOCATION

POSTRAW_DFR_DOMINATION:
  UNRESOLVED

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

This turn removes a misleading DFR narrative.

The candidate does not create a new probabilistic fusion failure mode: the five rawModSwitch events are inherited exactly, carry correction is pathwise, and reconstruction is an exact reuse of the same recrypt-key error.

But the candidate also cannot inherit the prior DFR for free, because RM10/joint recovery changes deterministic propagation of the already-sampled ciphertext/evaluation-key errors.

If the pending paired benchmark is strong, the correct next DFR question is a post-raw HElib noise-bound domination theorem, not empirical counting of logical outputs or KS calls.
