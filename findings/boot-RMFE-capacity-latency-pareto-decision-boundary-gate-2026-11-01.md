# BOOT RMFE Capacity–Latency Pareto Decision-Boundary Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 17/25
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

\`BBBINGW/memory main@5554fdc07fca70fc1d9cea815697e3ae1073d11d\`.

Relevant durable prerequisites:
- Turn 4 paired same-machine throughput contract;
- Turn 16 statistical estimand/resampling clarification;
- revised static capacity-ceiling gate.

## Primary hypothesis

A candidate may look favorable on latency alone but still lose the actual Aung-style throughput metric once final capacity is included.

This turn asks whether the full decision can be reduced to a simple pre-specified capacity–latency frontier, and whether one comparator can dominate the other.

Falsifier:
if the decision cannot be represented by fixed linear inequalities in candidate mean capacity and mean latency once comparator means are known.

## 1. Same-machine point-estimate frontier

Let the Turn-16 workflow-level means be:

\[
(\bar C_c,\bar T_c)
\]

for candidate,

\[
(\bar C_p,\bar T_p)
\]

for prior Corr./TnM, and

\[
(\bar C_t,\bar T_t)
\]

for thin.

Slot counts are:

\[
S_c=S_p=10,\qquad S_t=2.
\]

Aung-compatible throughput is

\[
\Theta_w
=
S_w\frac{\bar C_w}{\bar T_w}.
\]

Therefore the candidate beats Corr./TnM iff

\[
10\frac{\bar C_c}{\bar T_c}
>
10\frac{\bar C_p}{\bar T_p},
\]

equivalently

\[
\boxed{
\bar T_c
<
\frac{\bar T_p}{\bar C_p}\bar C_c
}
\]

or

\[
\boxed{
\bar C_c
>
\frac{\bar C_p}{\bar T_p}\bar T_c.
}
\]

The candidate beats thin iff

\[
10\frac{\bar C_c}{\bar T_c}
>
2\frac{\bar C_t}{\bar T_t},
\]

equivalently

\[
\boxed{
\bar T_c
<
5\frac{\bar T_t}{\bar C_t}\bar C_c
}
\]

or

\[
\boxed{
\bar C_c
>
\frac{\bar C_t}{5\bar T_t}\bar T_c.
}
\]

Thus the Strong-PASS point-estimate region is exactly

\[
\boxed{
\bar T_c
<
\bar C_c\cdot
\min\left(
\frac{\bar T_p}{\bar C_p},
5\frac{\bar T_t}{\bar C_t}
\right).
}
\]

Equivalently,

\[
\boxed{
\frac{\bar C_c}{\bar T_c}
>
\max\left(
\frac{\bar C_p}{\bar T_p},
\frac{\bar C_t}{5\bar T_t}
\right).
}
\]

So the capacity–latency decision boundary is linear once same-machine comparator means are known.

## 2. Which comparator is stricter?

Define comparator throughputs:

\[
\Theta_p=10\frac{\bar C_p}{\bar T_p},
\qquad
\Theta_t=2\frac{\bar C_t}{\bar T_t}.
\]

If

\[
\Theta_t>\Theta_p,
\]

then the thin frontier is stricter.

Proof:

\[
\Theta_t>\Theta_p
\]

is equivalent to

\[
\frac{\bar C_t}{5\bar T_t}
>
\frac{\bar C_p}{\bar T_p}.
\]

Hence any candidate beating thin automatically beats prior at the point-estimate level.

Conversely, if

\[
\Theta_p>\Theta_t,
\]

the prior-work frontier is stricter.

Therefore the first diagnostic on the pending artifact should be:

\[
\boxed{
\text{compare measured }\Theta_t\text{ and }\Theta_p.
}
\]

This determines which point-estimate frontier controls Strong PASS.

## 3. Exact ratio identity

The two candidate ratios satisfy:

\[
R_{\rm prior}
=
\frac{\Theta_c}{\Theta_p},
\]

\[
R_{\rm thin}
=
\frac{\Theta_c}{\Theta_t}.
\]

Hence

\[
\boxed{
R_{\rm thin}
=
R_{\rm prior}
\frac{\Theta_p}{\Theta_t}.
}
\]

This identity is useful for artifact auditing.

If the reported point estimates violate it beyond rounding error, the throughput analysis is internally inconsistent.

For every bootstrap replicate using a coherent resampling scheme, the same replicate-wise identity must hold:

\[
R_{\rm thin}^{*}
=
R_{\rm prior}^{*}
\frac{\Theta_p^{*}}{\Theta_t^{*}}.
\]

This is a cheap reproducibility check.

## 4. Published p=5 sanity frontier

Aung's printed p=5 values are:

Thin:

\[
C_t=151,\qquad T_t=2.82.
\]

Corr./TnM:

\[
C_p=101,\qquad T_p=11.3.
\]

Using the printed values:

\[
\Theta_t
\approx
107.09,
\]

\[
\Theta_p
\approx
89.38.
\]

Thus thin is clearly the stricter published frontier.

The candidate's allowable latency slopes are:

Prior frontier:

\[
\boxed{
T_c<0.111881\,C_c
}
\]

seconds.

Thin frontier:

\[
\boxed{
T_c<0.0933775\,C_c
}
\]

seconds.

Therefore, on the published-hardware sanity model, Strong PASS is controlled by thin.

Important:
these absolute-second values are **not** the pending same-machine decision rule. They are only a published-reference sanity map.

## 5. Published-reference frontier table

Using the printed Aung values:

| Candidate final capacity | Max latency to beat prior | Max latency to beat thin | Strong-PASS max |
|---:|---:|---:|---:|
| 70 | 7.832 s | 6.536 s | 6.536 s |
| 75 | 8.391 s | 7.003 s | 7.003 s |
| 80 | 8.950 s | 7.470 s | 7.470 s |
| 85 | 9.510 s | 7.937 s | 7.937 s |
| 90 | 10.069 s | 8.404 s | 8.404 s |
| 95 | 10.629 s | 8.871 s | 8.871 s |
| 100 | 11.188 s | 9.338 s | 9.338 s |
| 101 | 11.300 s | 9.431 s | 9.431 s |
| 105 | 11.748 s | 9.805 s | 9.805 s |
| 110 | 12.307 s | 10.272 s | 10.272 s |
| 115 | 12.866 s | 10.738 s | 10.738 s |

This table shows why latency-only interpretation is unsafe.

For example:
- at capacity 101, a 10.0 s candidate beats Corr./TnM but does not beat thin;
- at capacity 85, even 8.0 s is slightly too slow for the thin frontier.

## 6. Marginal exchange rate between capacity and latency

Using the printed p=5 thin comparator:

\[
T_c^{\max}
=
5\frac{2.82}{151}C_c.
\]

Therefore every one-bit reduction in final candidate capacity reduces the allowable latency by

\[
\boxed{
0.0933775\ {\rm s/bit}.
}
\]

Equivalently, every additional second of candidate latency requires

\[
\boxed{
10.7092\ {\rm capacity\ bits}
}
\]

to preserve thin-frontier throughput.

For prior Corr./TnM:

\[
0.111881\ {\rm s/bit}
\]

or

\[
8.93805\ {\rm bits/s}.
\]

These are useful sensitivity numbers, not absolute native thresholds.

## 7. Prior-only region

If thin throughput is above prior throughput, as in Aung's published p=5 data, then the point-estimate regimes are ordered:

\[
\Theta_c>\Theta_t
\Rightarrow
\Theta_c>\Theta_p.
\]

So there are only three point-estimate regions:

1. **Strong region**
   \[
   \Theta_c>\Theta_t>\Theta_p;
   \]

2. **Prior-only region**
   \[
   \Theta_t\ge\Theta_c>\Theta_p;
   \]

3. **No-prior-gain region**
   \[
   \Theta_c\le\Theta_p.
   \]

There is no point-estimate region in which the candidate beats thin but loses to prior when thin itself is faster than prior.

This ordering should be checked on the actual same-machine comparator results before interpreting the candidate.

## 8. CI interpretation remains separate

This turn does not replace Turn 16's bootstrap CI rule.

Even if the point estimate lies in the Strong region, a scientific Strong PASS still requires:

\[
CI_{95}^{lower}(R_{\rm prior})>1
\]

and

\[
CI_{95}^{lower}(R_{\rm thin})>1.
\]

Similarly, point-estimate comparator ordering does not by itself imply CI ordering because comparator uncertainty is sampled.

The frontier equations are:
- exact for point estimates;
- exact within each bootstrap replicate;
- useful for consistency and sensitivity;
- not a substitute for uncertainty analysis.

## 9. Capacity-only and latency-only misclassification examples

### Latency-only false optimism

Suppose candidate is much faster than prior:

\[
T_c<T_p,
\]

but capacity collapses enough that

\[
\frac{C_c}{T_c}
\le
\frac{C_p}{T_p}.
\]

Then candidate still loses prior throughput.

So:

\[
\boxed{
T_c<T_p
\not\Rightarrow
R_{\rm prior}>1.
}
\]

### Capacity-only false optimism

Likewise:

\[
C_c>C_p
\]

does not imply throughput superiority if latency grows enough.

Thus neither final capacity nor latency is a valid one-dimensional gate except for the previously established extreme capacity-only hard-kill floor.

## 10. Audit procedure when the pending result arrives

Before running any bootstrap:

1. verify execution contract and correctness;
2. compute:
   \[
   \Theta_c,\Theta_p,\Theta_t;
   \]
3. identify the stricter comparator;
4. verify:
   \[
   R_{\rm thin}
   =
   R_{\rm prior}\Theta_p/\Theta_t;
   \]
5. plot/place \((\bar C_c,\bar T_c)\) relative to both linear frontiers;
6. only then apply Turn-16 percentile/BCa CI decision rules.

This gives an immediate mechanism-level interpretation:
- capacity-limited;
- latency-limited;
- prior-only;
- or true cross-thin frontier movement.

## Verdict

\`\`\`text
RESULT:
  PASS_EXACT_CAPACITY_LATENCY_PARETO_BOUNDARY

BEAT_PRIOR_IFF:
  T_c < (T_prior/C_prior) * C_c

BEAT_THIN_IFF:
  T_c < 5*(T_thin/C_thin) * C_c

STRONG_POINT_ESTIMATE:
  ABOVE BOTH THROUGHPUT FRONTIERS

DOMINANT_COMPARATOR:
  WHICHEVER HAS HIGHER MEASURED THROUGHPUT

RATIO_IDENTITY:
  R_thin = R_prior * Theta_prior / Theta_thin

PUBLISHED_P5_ORDER:
  THIN > CORR/TNM
  THIN FRONTIER STRICTER

PUBLISHED_P5_THIN_SLOPE:
  0.0933775 sec / capacity-bit

PUBLISHED_P5_CAPACITY_COST_PER_SECOND:
  10.7092 bits / sec

LATENCY_ONLY_GATE:
  INVALID

CAPACITY_ONLY_GATE:
  INVALID EXCEPT EXTREME HARD-KILL FLOOR

CI_RULES:
  TURN16 PRESERVED

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The pending native result should be interpreted as a two-dimensional capacity–latency point, not as a speed benchmark with capacity attached afterward.

If the same-machine thin comparator remains above Corr./TnM, crossing the thin throughput frontier is the decisive point-estimate condition and automatically implies a prior-work point-estimate win.

The bootstrap CI is still required for scientific PASS.
