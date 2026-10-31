# BOOT RMFE Delayed-Fusion Scaling / Asymptotic Ceiling Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 13/25
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

\`BBBINGW/memory main@d31abebc1ace025180a1e7bf0744de3a3fda408a\`.

Relevant durable prerequisites:
- odd-prime / arbitrary-branch delayed-fusion generality;
- rawModSwitch compact carry-state gate;
- rawModSwitch dataflow work-compression gate;
- exact common recrypt-key reconstruction;
- current p=5 joint recovery construction;
- completed historical R4 timer decomposition.

## Primary hypothesis

The family-general delayed-fusion mechanism may asymptotically remove the \(k\)-fold MultKey cost, rather than merely reducing a constant factor.

Falsifier:
under the pinned stock HElib dataflow, identify any source-faithful per-branch work that remains \(\Theta(k)\) even after maximal exact post-raw fusion.

## 1. Stage decomposition

For one split thin branch, separate the MultKey-side work into:

### Unavoidable pre-fusion branch work

\[
F_{\rm raw}
=
\text{SlotsToCoeff / canonicalization}
+
\text{reLinearize}(s_R)
+
\text{rawModSwitch integer recovery}.
\]

For the exact HElib path, rawModSwitch itself contains two ciphertext parts and therefore two branch-local:

- \`DoubleCRT::toPoly\` conversions;
- coefficientwise scale/round/plaintext-correction loops.

### Post-raw branch work in stock Corr./TnM

After rawModSwitch, stock branch \(i\) performs:

\[
F_{\rm post}
=
\text{newMakeDivisible/divide}
+
\text{boot-key reconstruction}
+
\text{CoeffToSlots / inverse recovery}.
\]

The current delayed-fusion candidate preserves \(F_{\rm raw}\) branchwise but fuses \(F_{\rm post}\) after the raw boundary.

## 2. Exact source-level count for k branches

Each branch has two raw-switched parts.

Under the pinned HElib implementation:

### Stock k-branch path

- \`DoubleCRT::toPoly\`: \(2k\);
- raw coefficient rounding loops: \(2k\);
- \`powerfulToZZX\`: \(2k\);
- \`newMakeDivisible/divide\`: \(2k\);
- common-boot-key reconstruction: \(k\);
- branch-local inverse/C2S recovery: \(k\) copies.

### Delayed-fusion path

- \`DoubleCRT::toPoly\`: \(\boxed{2k}\);
- raw coefficient rounding loops: \(\boxed{2k}\);
- persistent branch raw ZZX materialization: can be streamed away;
- \`powerfulToZZX\`: at most \(\boxed{2}\);
- aggregate \`newMakeDivisible/divide\`: \(\boxed{2}\);
- common-boot-key reconstruction: \(\boxed{1}\);
- downstream recovery: one packed/restricted recovery problem.

Thus the exact fusion savings before the downstream recovery are:

\[
\boxed{
\begin{aligned}
\texttt{powerfulToZZX}:&\quad 2k\to2,\\
\text{divisibility passes}:&\quad 2k\to2,\\
\text{reconstruction}:&\quad k\to1.
\end{aligned}
}
\]

But:

\[
\boxed{
\texttt{toPoly}:2k\to2k
}
\]

and

\[
\boxed{
\text{raw rounding loops}:2k\to2k.
}
\]

## 3. Why the retained 2k work is structural for the current source design

The compact-carry theorem shows that one need not retain all branch raw outputs.

It does **not** remove the need to know each branch's local representative/rounding decisions.

Those decisions depend on the branch's centered integer coefficients recovered by \`DoubleCRT::toPoly\`.

The aggregate DCRT state is insufficient to reconstruct them exactly, because rawModSwitch is non-additive and Turn 5 established an aggregate-only impossibility.

Therefore, under the current HElib API/dataflow:

\[
\boxed{
\text{the 2k DCRT-to-integer conversions are retained source-faithfully}.
}
\]

This is not a universal lower bound on every possible RNS implementation.

A future algorithm that derives the compact carry state directly from branch RNS residues could change this conclusion, but no such algorithm is established.

## 4. Asymptotic consequence with context fixed

Fix:
- cyclotomic dimension \(N=\phi(m)\);
- active CRT-prime count \(L\);
- plaintext/recryption parameters.

One \`toPoly\` contains:
- one inverse FFT per active CRT prime;
- one coefficientwise integer CRT reconstruction.

Write its positive cost as

\[
C_{\rm toPoly}(N,L)>0.
\]

Then the delayed-fusion middle path contains the unavoidable term

\[
2k\,C_{\rm toPoly}(N,L),
\]

plus \(2k\) branch rounding passes.

Hence, with the HElib representation fixed:

\[
\boxed{
T_{\rm cand}(k)=\Omega(k).
}
\]

The stock k-branch path is also \(\Omega(k)\).

Therefore the delayed-fusion mechanism by itself does **not** change the asymptotic dependence on branch count from \(O(k)\) to \(O(1)\).

The defensible claim is a reduction in the coefficient of the \(k\)-linear work and removal of specific \(k\)-fold post-raw stages.

## 5. Current p=5 recovery does not change that conclusion

For the implemented p=5 candidate, post-reconstruction recovery is:

\[
10\text{ RM10 direct KS}
+
4\text{ chained joint-recovery KS}.
\]

This is \(14\) physical KS under BSGS+10 for the fixed \(k=5\) instance.

Its existence makes the p=5 constant-factor savings large.

It does not prove a general \(O(1)\) recovery cost as \(k\) varies.

Indeed Aung Proposition 3 gives \(k\) Frobenius terms for a generic rank-\(k\) linear map, so a family-general recovery may itself scale with \(k\).

Thus:

\[
\boxed{
\text{no family-level }k\to1\text{ asymptotic MultKey claim is justified}.
}
\]

## 6. Precise claim boundary

Do not claim:

\[
\text{"we remove the k-fold MultKey cost."}
\]

Do not claim:

\[
\text{"MultKey becomes independent of k."}
\]

Do not claim:

\[
\text{"rawModSwitch is fused from k branches to one."}
\]

The correct statement is:

> We preserve the branch-local rawModSwitch decisions, then collapse the **post-raw divisibility/reconstruction and packed recovery portion** into one aggregate path.

Equivalently:

\[
\boxed{
\text{k-way raw front-end retained}
\quad+\quad
\text{post-raw k-way tail collapsed}.
}
\]

## 7. Why this does not kill systems value

The absence of an asymptotic class change does not imply a small practical effect.

Historical completed R4 decomposition for the current p=5,w=512 regime reported:
- five-branch S2C median: \(0.03952\) s;
- retained pre/reconstruction-front median: \(0.16552\) s;
- reconstruction median: \(0.01899\) s;
- C2S median: \(2.86874\) s;
- total decomposed middle median: \(3.09244\) s;
- retained-share statistic \(\rho_{\rm ret}\approx0.06649923\).

Under that historical decomposition, the stage targeted by the current recovery redesign is overwhelmingly dominant, while the retained branch-local front is small.

The corresponding idealized middle-stage ceiling

\[
1/\rho_{\rm ret}
\approx15.04
\]

is only a sanity ceiling, not a candidate speedup prediction.

It does show that the retained \(\Theta(k)\) work does not statically kill the current p=5 systems opportunity.

The pending paired same-machine native task remains the decisive value gate.

## 8. Scaling interpretation across Aung's odd-prime family

Turn 12 established fusion semantics for all Aung odd-prime settings.

This turn adds:

- **semantic generality:** yes;
- **source-level asymptotic k-to-1 improvement:** no;
- **constant-factor opportunity:** parameter-dependent.

For larger \(k\):
- more post-raw reconstructions/divisibility passes are removed;
- but more branch-local toPoly/rounding work is also retained;
- generic rank-\(k\) recovery may itself grow with \(k\).

Therefore the speedup ratio need not increase monotonically with \(k\).

A larger \(k\) is not automatically a more favorable regime.

## 9. Research consequence

If the pending p=5 task STRONG-PASSES, the next family-level systems question should not be:

> does speedup scale like k?

Instead it should be:

> for which \((p,k,w)\) regimes is the removed post-raw tail a sufficiently large fraction of MultKey to offset the retained branch-local raw front and packed recovery cost?

That is a Pareto/regime question, not an asymptotic theorem.

No such parameter sweep is authorized while the current native slot is occupied.

## Verdict

\`\`\`text
RESULT:
  PASS_EXACT_SCALING_BOUNDARY
  FAIL_K_TO_ONE_ASYMPTOTIC_MULTKEY_CLAIM

STOCK_HELIB_BRANCH_TO_POLY:
  2k

CANDIDATE_BRANCH_TO_POLY:
  2k

STOCK_BRANCH_ROUNDING_PASSES:
  2k

CANDIDATE_BRANCH_ROUNDING_PASSES:
  2k

POWERFUL_TO_ZZX:
  2k -> 2

DIVISIBILITY_PASSES:
  2k -> 2

COMMON_BOOTKEY_RECONSTRUCTION:
  k -> 1

CURRENT_P5_RECOVERY:
  14 PHYSICAL KS UNDER BSGS+10
  FIXED-INSTANCE RESULT

CANDIDATE_K_SCALING_UNDER_STOCK_DATAFLOW:
  Omega(k)

ASYMPTOTIC_K_INDEPENDENT_MULTKEY:
  NOT ESTABLISHED / FALSE FOR CURRENT SOURCE DATAFLOW

STRUCTURAL_CLAIM:
  K-WAY RAW FRONT-END RETAINED
  POST-RAW K-WAY TAIL COLLAPSED

HISTORICAL_R4_RETAINED_SHARE:
  ~0.06649923
  IDEALIZED MIDDLE SPEEDUP CEILING ~15.04x
  SANITY CEILING ONLY

SYSTEMS_VALUE:
  STILL OPEN / NOT STATICALLY KILLED

FAMILY_SPEEDUP_MONOTONE_IN_K:
  NOT ESTABLISHED

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The delayed-fusion mechanism is family-general but should be sold as a **selective elimination of the post-raw k-fold tail**, not an asymptotic removal of all k-fold MultKey work.

Its publication value, if any, must come from:
- the obstruction-and-repair mechanism;
- a favorable practical cost distribution in meaningful regimes;
- measured frontier movement.

The current p=5 regime remains plausible precisely because historical profiling places most middle-path latency in the removable inverse/recovery portion.
