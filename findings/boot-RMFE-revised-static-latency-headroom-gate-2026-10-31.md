# BOOT RMFE Revised Static Latency-Headroom Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 14/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn asks one static value question:

> After Turns 8, 11, and 13 revised the candidate, can the branch be killed from published/source timing evidence alone, before the pending baseline timer returns?

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Updated throughput budget

Durable Aung p=5 correction/TnM baseline:

- SlotsToCtxts: 2.284 s
- MultKey: 4.732 s
- CtxtsToSlots: 0.078 s
- DigitExtract: 4.240 s
- final capacity: 101
- thin throughput frontier: 107.06 capacity-slots/s

The target total latency at capacity C is

\[
T_{\max}(C)=\frac{10C}{107.06}.
\]

At \(C=101\):

\[
T_{\max}=9.433962264\text{ s}.
\]

Turn 8's joint restricted recovery directly emits the main RMFE ciphertext and the correction-map outputs, so the old separate CtxtsToSlots stage is no longer required in the candidate.

Therefore fixed external latency is revised from

\[
2.284+0.078+4.240=6.602
\]

to

\[
T_{\rm fixed}=2.284+4.240=6.524\text{ s}.
\]

Hence the revised candidate middle-block budget is

\[
\boxed{
T_{\rm middle}<9.433962264-6.524
=2.909962264\text{ s}.
}
\]

Relative to the published 4.732 s MultKey block, the required reduction is

\[
1-\frac{2.909962264}{4.732}
=
\boxed{38.5046\%}.
\]

This supersedes the old 40.15% static target for the revised joint-recovery candidate.

## Current transform-side structural reduction

Five-branch baseline transform proxy:

\[
75
\]

automorphism/key-switch-scale calls.

Current revised candidate:

- 5 thin S2C calls;
- 10 RM10 calls;
- 4-call joint C2S/correction recovery.

Thus

\[
75\to19
\]

and the transform-side structural reduction is

\[
s_T
=
1-\frac{19}{75}
=
\boxed{74.6667\%}.
\]

Let \(f_T\) be the fraction of baseline MultKey latency attributable to the transform side.

If one ignores every other candidate saving and assumes transform-call latency scales proportionally with this count, transforms alone meet the revised 38.5046% block-reduction target when

\[
f_T s_T\ge0.385046.
\]

Therefore

\[
\boxed{
f_T\ge
\frac{0.385046}{0.746667}
=
0.515687.
}
\]

So a baseline transform-side share above about 51.6% would be sufficient even before crediting:

- 5->1 common boot-key reconstruction;
- 10->2 divisibility-lift passes;
- removal of persistent branch raw ZZX materialization.

Conversely, a much smaller transform share could still pass if those non-transform savings are material.

## Historical HElib sanity bracket

Halevi-Shoup's HElib bootstrapping report contains single-thread thin-bootstrapping timing tables, but the currently accessible live-indexed PDF and the cached mirror used by the research connector expose different table values for the linear-transform rows.

Therefore these historical transform-share numbers are **version-sensitive provenance** and must not be used quantitatively for the present gate.

Across either edition they are also different parameters and report total recrypt rather than Aung's p=5 MultKey block.

Conclusion:

\[
\boxed{\text{historical HElib transform timings are sanity evidence only}}
\]

and provide neither a static kill nor a static pass for the current candidate.

## Historical toPoly timer sanity check

A public HElib verbose timer log (GitHub issue #324, old parameters) reports approximately:

\[
\texttt{toPoly}: 269.022/5145
\approx0.05229\text{ s/call}.
\]

That run used approximately:

- \(\phi(m)=24000\);
- 11 ciphertext primes;
- single-thread execution;
- a much older/different HElib parameter set.

In the current pinned Aung rawModSwitch source path:

- \(\phi(m)=16384\);
- the ciphertext is explicitly mod-downed to at most 3 ciphertext primes immediately before rawModSwitch.

So the historical timer weakly suggests that ten current toPoly calls are unlikely by themselves to consume the entire 2.910 s candidate middle budget.

But this is only a cross-parameter sanity check. Hardware, source revision, prime sizes, cache behavior, and surrounding dataflow differ.

No hard latency bound is derived from it.

## Source-level unavoidable work

Turn 13 establishes that the current source-level candidate still requires:

- 5 thin S2C paths;
- 5 key-switch/reLinearize paths;
- 10 DoubleCRT::toPoly calls;
- 10 branch coefficient-rounding passes.

Current exact savings include:

- powerfulToZZX 10 -> <=2;
- newMakeDivisible/divide 10 -> 2 aggregate passes + carry correction;
- boot-key reconstruction 5 -> 1;
- inverse/recovery transform side compressed to RM10 + 4-call joint map;
- separate CtxtsToSlots removed.

The published and historical data contain no source-faithful timing split for these exact components at
\(m=32768,p=5,w=512,k=5\).

Therefore no rigorous positive lower bound on the retained candidate latency can be derived that exceeds 2.909962 s.

## Revised static kill criterion for the pending result

The old Turn-4 retained-share hard-kill ratio is superseded.

When the pending baseline timer returns, the source-faithful lower-bound core should be built from components that remain proven unavoidable:

\[
T_{\rm core}
=
T_{\rm S2C}
+
T_{\rm reLinearize}
+
T_{\rm toPoly}
+
T_{\rm branch-round-loop}
+
T_{\rm required\ modDown/canonicalization}.
\]

A hard latency kill requires, on a source-faithful comparable baseline,

\[
T_{\rm core}
+
T_{\rm minimum\ revised\ recovery}
\ge
2.909962\text{ s}
\]

after translating to the same performance basis.

The already-instrumented \`toPoly\`, \`toPoly_FFT\`, \`toPoly_CRT\`, and \`reLinearize\` timers materially improve this audit.

The pending task must not be rerun or modified.

## Verdict

\`\`\`text
RESULT:
  PASS_REVISED_STATIC_LATENCY_HEADROOM

REVISED_MIDDLE_BUDGET_AT_C101:
  2.909962 s

REQUIRED_MULTKEY_REDUCTION:
  38.5046%

TRANSFORM_COUNT:
  75 -> 19

TRANSFORM_REDUCTION:
  74.6667%

TRANSFORM_SHARE_NEEDED_IF_TRANSFORMS_ALONE_PAY_FOR_GAIN:
  51.5687%

STATIC_HARD_KILL:
  NO

STATIC_SPEEDUP_PROOF:
  NO

HISTORICAL_HELIB_TIMING:
  SUPPORTS PLAUSIBILITY ONLY / NON-TRANSFERABLE

PENDING_BASELINE_TIMER:
  GENUINELY DECISIVE / DO NOT RERUN

NATIVE_LATENCY:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The revised candidate cannot be killed from current static timing evidence.

But neither operation counts nor historical HElib data justify a speedup claim.

The pending timer is not merely confirmatory: it is now the first source-faithful measurement capable of determining whether the retained 10 toPoly conversions + branch-local key-switch/rounding core leave enough headroom for the revised recovery.

Do not launch a candidate native implementation before that result is independently audited.

## Next independent side-research

If the timer remains pending, the highest-information static question should shift from latency to capacity:

- derive a **revised optimistic whole-pipeline capacity ceiling** for the current 19-call candidate;
- combine known 15.740880-bit joint-recovery multiplier tax with conservative key-switch/RM10 bounds;
- kill if even optimistic final capacity drops enough that the throughput target becomes unreachable.

AI_PROVISIONAL_CHOICE:
  RETAIN_REVISED_POSTRAW_FUSION_PENDING_TIMER
  STOP_STATIC_LATENCY_MICRO-OPTIMIZATION
  NEXT_STATIC_PRIORITY = REVISED_CAPACITY_CEILING_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
