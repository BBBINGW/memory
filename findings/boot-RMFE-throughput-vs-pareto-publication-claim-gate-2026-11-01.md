# BOOT RMFE Throughput-vs-Pareto Publication-Claim Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 18/25
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

\`BBBINGW/memory main@f8dc16d5352867226361e44e48342ae203f22e10\`.

Relevant durable prerequisites:
- Turn 4 paired same-machine throughput contract;
- Turn 16 statistical inference clarification;
- Turn 17 capacity-latency frontier;
- Turn 3 Part 2 BSGS+10 evaluation-key byte bound;
- Turn 15 post-Aung novelty search.

## Primary hypothesis

A Strong PASS under Aung's throughput metric may be sufficient to claim that the candidate strictly advances the practical FHE Pareto frontier over both Aung Corr./TnM and vanilla thin bootstrapping.

Falsifier:
construct a candidate with higher Aung throughput but worse primitive metrics such as latency, final capacity / remaining depth, or evaluation-key size.

## 1. Aung explicitly treats throughput and remaining multiplicative depth as distinct metrics

Aung et al. ePrint 2025/350 physical pp24--26 reports:
- final ciphertext capacity;
- remaining multiplications;
- latency;
- throughput.

Their throughput metric is

\[
\Theta
=
\frac{\text{post-bootstrap capacity}\times \#\text{slots}}
     {\text{latency}}.
\]

Separately, they measure the number of rounds of squaring that can be performed before decryption fails, and report the minimum among ten runs as "Remaining Mults".

Aung's discussion explicitly notes that some workflows can have competitive throughput while leaving very few multiplications, and says the correction-map technique is important in practice because it raises the number of remaining multiplications.

Therefore:

\[
\boxed{
\text{throughput does not subsume remaining-depth utility}.
}
\]

The paper itself treats them as distinct practical axes.

## 2. Throughput dominance is not primitive-metric dominance

For workflow \(w\), Aung throughput is

\[
\Theta_w=S_w C_w/T_w.
\]

A candidate can have

\[
\Theta_c>\Theta_t
\]

while simultaneously having

\[
C_c<C_t
\]

and

\[
T_c>T_t.
\]

The larger slot count \(S_c\) can compensate for both disadvantages.

Concrete published-reference witness:

Thin p=5:

\[
S_t=2,\qquad C_t=151,\qquad T_t=2.82.
\]

Consider the hypothetical candidate:

\[
S_c=10,\qquad C_c=90,\qquad T_c=8.
\]

Then

\[
\Theta_c
=
10\cdot90/8
=
112.5,
\]

whereas the printed thin throughput is approximately

\[
107.06.
\]

Thus:

\[
\Theta_c>\Theta_t
\]

even though:

\[
T_c> T_t
\]

and

\[
C_c<C_t.
\]

So:

\[
\boxed{
\text{Aung-throughput Strong PASS}
\not\Rightarrow
\text{latency dominance}
}
\]

and

\[
\boxed{
\text{Aung-throughput Strong PASS}
\not\Rightarrow
\text{capacity dominance}.
}
\]

## 3. It also does not prove remaining-multiplication dominance

Aung's p=5 published rows illustrate that capacity and remaining multiplications are correlated but not interchangeable labels:

- thin: final capacity 151, remaining mults 8;
- Corr./TnM: 101, remaining mults 5;
- Corr./BSGS: 115, remaining mults 6;
- Naive/BSGS: 58, remaining mults 2.

The remaining-multiplication metric is obtained by actually applying additional squarings until decryption fails.

The current pending task records final capacity but Turn 4 did not require a post-bootstrap repeated-squaring depth test.

Therefore a Strong PASS from the pending task does **not** establish:

\[
M_c\ge M_t
\]

or even

\[
M_c\ge M_p.
\]

Do not infer a discrete remaining-multiplication count from final capacity alone.

If systems value survives, remaining multiplications is a separate follow-up measurement.

## 4. Equal-keyset runtime fairness is not equal deployment key size

Turn 4 deliberately requires all three timed workflows to use the same BSGS+10 evaluation-key set.

This is the correct runtime fairness rule:
- the candidate does not get a direct-key advantage unavailable to comparators;
- Corr./TnM itself can benefit from added direct matrices.

But this benchmark design does not imply that the deployed stock comparators intrinsically require those ten extra RM10 matrices.

Turn 3 Part 2 established that the candidate-specific BSGS+10 augmentation adds:
- exactly 10 direct Frobenius KeySwitch matrices;
- +5.555556% Frobenius DCRT payload;
- <5.557% whole serialized PubKey overhead relative to a BSGS public key already containing the 180 ordinary direct Frobenius matrices.

Therefore two different statements must be separated.

### Runtime comparison

Use the same BSGS+10 keyset for all workflows.

### Deployment/storage comparison

Report the candidate-specific extra ten matrices relative to a stock comparator that could omit them.

Hence a same-keyset runtime benchmark does **not** justify:

> "the candidate has the same evaluation-key size as stock thin/Corr.-TnM."

The scientifically correct statement is:

> Runtime is compared under an equal augmented keyset; deploying the candidate requires ten additional direct automorphism matrices, statically bounded at <5.557% serialized-PubKey overhead relative to the BSGS baseline.

## 5. Strict Pareto dominance definition

For a fixed security/correctness regime, define primitive benefit axes:

\[
S=\text{logical packed slots},
\]

\[
C=\text{post-bootstrap capacity},
\]

\[
M=\text{remaining multiplications},
\]

and cost axes:

\[
T=\text{latency},
\qquad
K=\text{evaluation/public-key bytes},
\qquad
R=\text{peak RSS}.
\]

A candidate strictly Pareto-dominates comparator \(b\) only if:

\[
S_c\ge S_b,
\quad
C_c\ge C_b,
\quad
M_c\ge M_b,
\]

\[
T_c\le T_b,
\quad
K_c\le K_b,
\quad
R_c\le R_b,
\]

with at least one strict inequality, under comparable security/correctness assumptions.

The current pending throughput gate does not measure all these coordinates.

Therefore:

\[
\boxed{
\text{Turn-4 Strong PASS is not a strict Pareto-dominance certificate.}
}
\]

## 6. What Strong PASS *does* establish

If Turn 4 + Turn 16 return Strong PASS, the strongest immediate claim is:

> Under one fixed same-machine BSGS+10 keyset/configuration, the candidate has statistically higher Aung-style capacity-times-packing throughput than both source-faithful Corr./TnM and vanilla thin.

This is a real systems result.

It means:

\[
\boxed{
\Theta_c>\Theta_p
\quad\text{and}\quad
\Theta_c>\Theta_t
}
\]

with the prescribed uncertainty rule.

It does **not** mean:
- lower latency than thin;
- more capacity than thin;
- more remaining multiplications than thin;
- smaller evaluation key than thin;
- lower RSS than thin.

## 7. "Pareto frontier movement" has two possible meanings

### Strict primitive-axis frontier movement

This requires demonstrating that the new point is non-dominated in the chosen primitive metric vector and, for a dominance claim over a named comparator, satisfying the coordinate-wise inequalities above.

The pending gate alone is insufficient because \(M\) and deployment \(K/R\) are not fully measured.

### Application-weighted/composite frontier crossing

Aung throughput already defines one utility projection:

\[
\Theta=S C/T.
\]

A Strong PASS can legitimately be called:

\[
\boxed{
\text{crossing the Aung throughput frontier}.
}
\]

This is the preferred phrase before full multi-dimensional closure.

It should not be shortened to "dominates thin bootstrapping".

## 8. Non-dominance versus dominance against thin

Vanilla thin has only

\[
S_t=2
\]

logical slots in the p=5 benchmark, versus

\[
S_c=10
\]

for the RMFE candidate.

If slot count is treated as a genuine benefit axis, thin cannot strictly dominate an otherwise correct candidate with 10 slots, because

\[
S_t<S_c.
\]

Conversely, the candidate cannot claim strict dominance over thin unless it also matches/exceeds thin on the other selected benefit/cost axes.

Thus a realistic Strong-PASS outcome will often mean:

\[
\boxed{
\text{a new non-dominated tradeoff point},
}
\]

not:

\[
\boxed{
\text{thin is obsolete/dominated}.
}
\]

This distinction is consistent with the motivation of RMFE/FIMD: trading packing against bootstrapping cost.

## 9. Comparison against Corr./TnM is stronger, but key-size caveat remains

Candidate and Corr./TnM both use

\[
S=10
\]

logical slots for p=5,w=512,k=5.

Therefore a candidate with:
- lower latency;
- at least equal final capacity;
- at least equal remaining multiplications

would be close to primitive-axis dominance on the main online metrics.

However, stock Corr./TnM does not inherently need all ten candidate RM10 direct keys.

So even in this favorable case the candidate should report a key-size tradeoff rather than claim unconditional all-axis dominance, unless a deployment comparison shows the overhead is eliminated or irrelevant under a common required keyset.

## 10. Publication-value decision matrix after native result

### Case A — Strong throughput PASS, plus healthy depth

If:
- Turn-16 Strong PASS over prior and thin;
- final capacity remains useful;
- later remaining-multiplication measurement is practically healthy;

then the result supports:

> obstruction-aware delayed fusion creates a new RMFE bootstrapping tradeoff point that crosses the previous Aung throughput frontier, with a bounded additional evaluation-key cost.

This is compatible with a paper-level systems contribution if novelty closure also survives.

### Case B — Strong throughput PASS but very low remaining depth

Then the candidate may be a mathematically valid high-throughput point but practically weak.

Do not call it a strong frontier advance solely from \(\Theta\).

Aung's own discussion treats very low remaining multiplication counts as a practical limitation.

### Case C — Prior-only PASS

Turn 4 already classifies this as low publication value.

Turn 18 strengthens the interpretation:
it is an engineering improvement inside the RMFE family, not a cross-thin frontier result.

### Case D — No prior-work gain

Kill systems value under this regime, unchanged from Turn 4.

## 11. Required language if the pending task Strong-PASSES

Safe:

> Candidate throughput exceeds both Corr./TnM and thin under the same-machine Aung metric.

Safe if supported:

> The candidate establishes a new non-dominated RMFE tradeoff point.

Preferred until depth/key/RSS closure:

> The candidate crosses the Aung capacity-times-packing throughput frontier.

Unsafe without additional evidence:

> The candidate dominates thin bootstrapping.

Unsafe:

> The candidate is faster than thin.

unless

\[
T_c<T_t
\]

is separately true.

Unsafe:

> The candidate has more usable post-bootstrap depth than thin.

unless remaining-multiplication evidence establishes it.

Unsafe:

> There is no key-size tradeoff.

## Verdict

\`\`\`text
RESULT:
  FAIL_THROUGHPUT_PASS_IMPLIES_STRICT_PARETO_DOMINANCE
  PASS_COMPOSITE_FRONTIER_CLAIM_BOUNDARY

TURN4_STRONG_PASS_ESTABLISHES:
  HIGHER AUNG CAPACITY*PACKING/LATENCY THROUGHPUT
  UNDER FIXED SAME-MACHINE KEYSET/CONFIGURATION

STRICT_LATENCY_DOMINANCE:
  NOT IMPLIED

STRICT_CAPACITY_DOMINANCE:
  NOT IMPLIED

REMAINING_MULTIPLICATION_DOMINANCE:
  NOT MEASURED BY PENDING TASK

DEPLOYMENT_KEY_SIZE:
  CANDIDATE REQUIRES +10 DIRECT MATRICES
  <5.557% SERIALIZED-PUBKEY OVERHEAD VS BSGS BASELINE

EQUAL-KEYSET BENCHMARK:
  FAIR FOR RUNTIME
  DOES NOT ERASE CANDIDATE-SPECIFIC DEPLOYMENT KEY COST

SAFE FRONTIER LANGUAGE AFTER STRONG PASS:
  CROSSES AUNG THROUGHPUT FRONTIER

STRICTLY DOMINATES THIN:
  NOT ESTABLISHED BY TURN4

LIKELY SCIENTIFIC INTERPRETATION:
  NEW NON-DOMINATED TRADEOFF POINT
  IF DEPTH REMAINS PRACTICALLY USEFUL

FOLLOW-UP IF STRONG PASS:
  MEASURE REMAINING MULTIPLICATIONS
  REPORT ABSOLUTE KEY BYTES/RSS
  THEN ASSESS FULL PRIMITIVE-AXIS PARETO STATUS

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Aung throughput is the correct primary gate because it reflects the central FIMD motivation: capacity and packing amortized over latency.

But a win on that scalar utility function must be reported as a composite throughput-frontier win, not as universal superiority.

The strongest paper story, if native performance succeeds, is likely a new tradeoff point enabled by a structural obstruction-and-repair mechanism, with explicit depth and evaluation-key tradeoffs.
