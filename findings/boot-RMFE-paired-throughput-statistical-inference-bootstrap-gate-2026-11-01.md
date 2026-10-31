# BOOT RMFE Paired-Throughput Statistical Inference / Bootstrap Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 16/25
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

\`BBBINGW/memory main@4a24324e3e10de67a2af87d353f68405d272a784\`.

Relevant durable prerequisites:
- Turn 4 paired same-machine throughput native-gate contract;
- Turn 6 key-conditioning / DFR event-graph gate;
- Turn 8/9 proof that HElib final noise/capacity can depend on actual ciphertext digit decompositions;
- Turn 14 execution-contract pre-audit.

## Primary hypothesis

Turn 4's performance decision can be made statistically sound from 20 measured invocations per workflow using a deterministic bootstrap CI on the throughput ratios.

Falsifier:
show that a naive bootstrap or naive per-run-ratio analysis changes the estimand, destroys relevant dependence, or claims uncertainty coverage that the experiment does not actually sample.

## 1. Aung's throughput estimand is an aggregate metric, not a per-run ratio

Aung et al. define

\[
\Theta
=
\frac{C\cdot S}{T},
\]

where:
- \(C\) is post-bootstrap capacity;
- \(S\) is the number of packed slots;
- \(T\) is latency.

Their experimental section explicitly says:

> Latency is the average time taken (in seconds) for the bootstrapping workflow to complete.

The reported Table 3 throughputs are numerically consistent, up to printed rounding, with

\[
\frac{\text{reported capacity}\times \text{slots}}
     {\text{reported average latency}}.
\]

For example, the printed p=5 thin row gives

\[
151\cdot2/2.82\approx107.09
\]

versus reported 107.06, and Corr./TnM gives

\[
101\cdot10/11.3\approx89.38
\]

versus 89.08. The small discrepancies are compatible with using unrounded internal capacity/latency values.

Therefore the closest same-machine extension of Aung's metric is a **ratio of workflow-level aggregates**, not the mean of invocation-level ratios.

## 2. Pre-specified primary estimand for the pending gate

For workflow \(w\), with measured invocations \(i=1,\ldots,n\), define

\[
\bar C_w
=
\frac1n\sum_i C_{w,i},
\qquad
\bar T_w
=
\frac1n\sum_i T_{w,i}.
\]

Define the Aung-compatible plug-in throughput

\[
\boxed{
\widehat\Theta_w
=
S_w
\frac{\bar C_w}{\bar T_w}.
}
\]

For the current p=5 comparison:

\[
S_{\rm cand}=S_{\rm prior}=10,
\qquad
S_{\rm thin}=2.
\]

Hence

\[
\boxed{
\widehat R_{\rm prior}
=
\frac{\bar C_{\rm cand}\bar T_{\rm prior}}
     {\bar C_{\rm prior}\bar T_{\rm cand}}
}
\]

and

\[
\boxed{
\widehat R_{\rm thin}
=
5
\frac{\bar C_{\rm cand}\bar T_{\rm thin}}
     {\bar C_{\rm thin}\bar T_{\rm cand}}.
}
\]

This makes Turn 4's scalar formulas precise: every \(C,T\) in those formulas should be interpreted as the measured workflow mean unless the capacity is exactly invariant across runs.

## 3. Mean per-run throughput is a different estimand

The alternative

\[
\frac1n\sum_i S_w\frac{C_{w,i}}{T_{w,i}}
\]

is generally not equal to

\[
S_w\frac{\bar C_w}{\bar T_w}.
\]

A two-run counterexample:

\[
(C_1,T_1)=(1,1),
\qquad
(C_2,T_2)=(100,10).
\]

Then

\[
\frac12\left(\frac11+\frac{100}{10}\right)=5.5,
\]

whereas

\[
\frac{(1+100)/2}{(1+10)/2}
=
\frac{50.5}{5.5}
\approx9.18.
\]

Therefore:
- mean per-run throughput may be reported as a secondary descriptive metric;
- it must not silently replace the Aung-compatible primary metric.

The same applies to medians.

## 4. Capacity and latency must be resampled jointly within an invocation

Pinned HElib source shows that final \`noiseBound\`, hence final capacity, can depend on the actual ciphertext state.

In \`Ctxt::keySwitchPart\`:

\[
\texttt{addedNoise}
=
\texttt{breakIntoDigits(actual\ part)}
\cdot
W.\texttt{noiseBound},
\]

and this value is added to the ciphertext ledger.

Therefore \(C_{w,i}\) is not guaranteed to be constant across fresh ciphertext invocations.

Also, \(C_{w,i}\) and \(T_{w,i}\) arise from the same execution and can be statistically dependent.

A valid bootstrap must therefore resample the pair

\[
\boxed{
(C_{w,i},T_{w,i})
}
\]

as one observation.

It is invalid to:
- bootstrap the capacity array independently from the latency array;
- shuffle capacity and latency relative to each other;
- compute separate CIs for \(C\) and \(T\) and combine interval endpoints algebraically.

Each bootstrap replicate must recompute

\[
\widehat\Theta_w^*
=
S_w
\frac{\bar C_w^*}{\bar T_w^*}
\]

from resampled invocation pairs.

## 5. Paired versus independent resampling across workflows

The word "paired" in Turn 4 primarily meant same-machine/same-keyset comparison.

It does **not automatically mean** the statistical observations are paired.

### Use paired bootstrap only if the artifact deliberately creates matched trial blocks

Examples:
- candidate and prior both start from copies of the same RMFE ciphertext for trial \(i\);
- all workflows in trial \(i\) are generated from one pre-recorded trial seed/block;
- workflow order is interleaved within that block.

Then one should resample trial blocks jointly, preserving the within-block covariance.

For candidate vs prior, a true same-ciphertext pairing is especially natural because both have the same RMFE logical input format.

### Use independent bootstrap if there is no deliberate matching

If the workflow arrays are simply:
- 20 fresh candidate ciphertexts;
- 20 unrelated prior ciphertexts;
- 20 unrelated thin ciphertexts;

then matching element 7 with element 7 has no statistical meaning.

The bootstrap must resample workflow arrays independently.

\[
\boxed{
\text{array index equality is not evidence of pairing}.
}
\]

For thin versus RMFE, the ciphertext packing differs, so a paired analysis requires an explicitly defined common trial block; it cannot be inferred from the run number.

## 6. Fixed-keyset scope

The Turn 4 contract intentionally requires the same BSGS+10 evaluation-key set for all workflows.

If one keyset \(K\) is generated once and all 20 measurements reuse it, the resulting CI estimates invocation/runtime variation **conditional on that keyset**:

\[
\Pr_{X,\tau,\text{runtime}}[\cdot\mid K].
\]

It does not estimate uncertainty over fresh key generation:

\[
K\leftarrow\text{KeyGen}.
\]

This matters because:
- evaluation-key errors are sampled once at key generation;
- final capacity can depend on those fixed errors;
- the candidate uses eight candidate-only direct RM10 matrix-error directions identified in Turn 7.

Therefore a Strong PASS from the current task supports:

> same-machine throughput dominance for the measured fixed keyset/configuration.

It does **not by itself** support:

> key-averaged throughput dominance over fresh evaluation keys.

A multi-key experiment would be required for the latter.

This limitation does not invalidate the current bounded systems gate; it defines its inferential scope.

## 7. Measurement-order confounding

Same-machine execution removes hardware-generation mismatch, but not necessarily time/order drift.

If workflows are measured in three long blocks, for example:

\[
20\times\text{thin}
\to
20\times\text{prior}
\to
20\times\text{candidate},
\]

then:
- CPU frequency;
- thermal state;
- background load;
- cache/page state

can be partially confounded with workflow identity.

A standard iid bootstrap of within-workflow arrays does not capture an unobserved workflow-order effect.

The strongest design is randomized/interleaved trial blocks, e.g. one permutation of the three workflows per trial.

The pending task must not be changed now.

When its artifact arrives:
- record exact workflow execution order;
- if randomized/interleaved, paired/block resampling is preferred;
- if blockwise, the result remains useful but the CI should be described as conditional on that execution order.

A blockwise run is not automatically \`FAIL_EXECUTION_CONTRACT\` because Turn 4 did not pre-specify interleaving, but a marginal result close to \(R=1\) should be treated conservatively.

## 8. Deterministic bootstrap prescription

To remove ambiguity before seeing the native result, use the following analysis if the raw invocation arrays are available.

### Primary statistic

\[
\widehat R_{\rm prior},
\widehat R_{\rm thin}
\]

defined from workflow mean capacities and mean latencies.

### Resampling unit

One measured invocation pair

\[
(C_i,T_i)
\]

or one deliberate matched trial block.

### Bootstrap

- \(B=100000\) resamples;
- fixed seed \`20261101\`;
- recompute all workflow means and the ratio statistic in every resample;
- report percentile 95% CI.

### Robustness sensitivity

Also compute:
- BCa 95% CI if numerically well-defined;
- median of invocation-level throughputs as descriptive secondary output.

If percentile and BCa place the decision threshold \(1\) on different sides, classify the performance result as

\[
\boxed{\texttt{UNCLEAR}}
\]

rather than selecting the favorable interval.

This is conservative and prevents a 20-sample bootstrap-method choice from determining a paper-level conclusion.

## 9. Nonpositive-capacity boundary

The Aung-style metric assumes usable positive post-bootstrap capacity.

If a workflow has

\[
\bar C_w\le0,
\]

the ratio is not a meaningful positive-throughput comparison.

For the candidate:
- any correctness failure is already \`FAIL_NATIVE_CORRECTNESS\`;
- a correct but nonpositive-capacity candidate has no practical post-bootstrap headroom and should fail the systems-value gate rather than be rescued by a ratio convention.

No such result is assumed here.

## 10. Updated decision semantics

Turn 4's thresholds remain valid after replacing ambiguous \(C,T\) by the pre-specified aggregate estimators above.

### Strong PASS

\[
\operatorname{CI}^{\rm lower}_{95}(R_{\rm prior})>1
\]

and

\[
\operatorname{CI}^{\rm lower}_{95}(R_{\rm thin})>1.
\]

Interpretation must include:
- fixed measured keyset;
- measured runtime/order configuration;
- chosen resampling structure.

### Prior-only PASS / thin FAIL

Same Turn-4 rule.

### No-prior gain

Same Turn-4 rule.

### UNCLEAR

Also include:
- CI straddles 1;
- percentile/BCa classification disagreement;
- missing raw arrays preventing valid joint \((C,T)\) resampling;
- ambiguous run matching that prevents deciding paired vs independent bootstrap.

## 11. Required artifact evidence

The eventual artifact should expose enough information to reproduce the statistical verdict:

- per-invocation \(C_i\);
- per-invocation \(T_i\);
- correctness bit;
- workflow identifier;
- trial/run identifier;
- keyset identifier/hash;
- whether candidate/prior share the same input ciphertext copy;
- input/trial seed if recorded;
- exact workflow execution order;
- warmup exclusion;
- analysis seed and bootstrap script/output.

If only means are reported, one can compute point ratios but not the pre-specified CI.

## Verdict

\`\`\`text
RESULT:
  PASS_BOOTSTRAP_CI_WITH_REQUIRED_ESTIMAND_AND_RESAMPLING_CLARIFICATION

PRIMARY_WORKFLOW_THROUGHPUT:
  slots * mean(capacity) / mean(latency)

MEAN_PER_RUN_CAPACITY_OVER_LATENCY:
  SECONDARY ONLY
  DIFFERENT ESTIMAND

BOOTSTRAP_UNIT_WITHIN_WORKFLOW:
  JOINT (capacity_i, latency_i) INVOCATION

PAIRED_CROSS_WORKFLOW_BOOTSTRAP:
  ONLY IF DELIBERATE MATCHED TRIAL BLOCK EXISTS

INDEPENDENT_CROSS_WORKFLOW_BOOTSTRAP:
  REQUIRED OTHERWISE

FIXED_KEYSET_CI_SCOPE:
  CONDITIONAL ON MEASURED KEYSET
  NOT KEY-AVERAGED

WORKFLOW_ORDER:
  MUST BE REPORTED
  BLOCKWISE ORDER CAN CONFUND SMALL EFFECTS

BOOTSTRAP_REPLICATES:
  100000

BOOTSTRAP_SEED:
  20261101

PRIMARY_CI:
  PERCENTILE 95%

SENSITIVITY_CI:
  BCA 95% WHEN DEFINED

PERCENTILE_VS_BCA_DECISION_DISAGREEMENT:
  UNCLEAR

RAW_ARRAYS_MISSING:
  POINT ESTIMATE ONLY / NO SCIENTIFIC CI PASS

TURN4_THRESHOLD_RULES:
  PRESERVED AFTER THIS CLARIFICATION

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The Turn-4 same-machine gate remains statistically usable, but its bootstrap must respect what was actually sampled.

The two most important audit rules when the pending result arrives are:

1. never separate capacity from its invocation latency during resampling;
2. never claim a paired bootstrap merely because workflow arrays have the same length/index.

A Strong PASS will be a conditional systems result for one fixed BSGS+10 keyset. That is sufficient for the current bounded decision gate, but not a key-averaged DFR or universal-performance theorem.
