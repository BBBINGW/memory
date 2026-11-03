# BOOT / B158 — Turn 21 — paper-level VALUE_REVIEW: p=5 correctness anchor versus family value anchor

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

VALUE_REVIEW_COMPLETED: true

## Authority / scope

GitHub Notes read-before-write was attempted first and remains degraded.
Exact Turn-20 durable finding:
    findings/boot-successor-turn20-fixed-ring-carrier-feasibility-table-all-correction-rows-2026-11-03.md
    commit 26413d32b4463d050400d0f6789a352617107c11
    blob 8f1d7b9dfa8b39273b66f2c253e1ce9af77994b5.

The target Turn-21 path was checked absent before write.
The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

This is a paper-level VALUE_REVIEW, not a benchmark and not a correctness rerun.

## Primary question

Does the active p=5,w=512,k=5 instance remain a credible paper anchor despite its approximately 1.5x idealized end-to-end speedup ceiling, now that Turn 20 shows the same representation mechanism forms a broader fixed-ring family with higher-k rows?

The answer should determine whether to:
- keep p=5 ACTIVE;
- PARK it;
- or keep it as correctness anchor while moving paper-value burden to the family.

## Inputs already established

Aung p=5,w=512 Corr./TnM:
    detailed total latency T_A =11.33 s
    Table-3 latency T_A3 =11.3 s
    post capacity C_A =101
    throughput ratio vs thin rho_A =0.832
    published MultKey stage M_A =4.732 s.

Idealized one-MultKey screening from Turn 18:
    T_ideal
      =11.33 -(4/5)*4.732
      =7.5444 s.

Idealized maximum p=5 latency speedup:
    11.33/7.5444
      =1.5017761518x.

At unchanged capacity101:
    idealized thin-throughput ratio
      =0.832*(11.3/7.5444)
      =1.2461693441.

Thus p=5 can in principle cross the thin-throughput frontier, but only with bounded recovery/guard overhead.

Turn 20 additionally proves a parameterized family:
- all 19 non-DNE correction rows are carrier-feasible;
- higher-k rows eliminate more split MultKeys for modestly larger recovery automorphism counts.

## 1. Objective value events, not arbitrary percentage thresholds

This review deliberately avoids declaring an arbitrary publication rule such as:
    "20% speedup is enough."

Instead use two source-defined frontier events.

### Event D: dominate the direct Aung p=5 correction point

For the UNGUARDED fast path, the candidate strictly improves the Aung p=5 latency/capacity point if:

    T_fast <11.33
and
    C_fast >=101,

with no worse correctness/security assumptions.

This is a meaningful direct-baseline improvement.

Equivalent overhead budget relative to the optimistic T_ideal:

    O_fast
      =T_fast-T_ideal
      <3.7856 s.

If C_fast<101, direct Pareto dominance is absent even if latency improves; then throughput/capacity tradeoff must be reported explicitly.

### Event T: cross Aung's thin-bootstrap throughput frontier

For the same k=5 packing:

    rho_fast
      =0.832*(C_fast/101)*(11.3/T_fast).

Crossing thin requires:

    rho_fast >1,

equivalently:

    T_fast
      <9.4016*(C_fast/101).                 (T21.1)

At C_fast=101:

    T_fast <9.4016 s.

Relative to T_ideal this permits only:

    O_fast <1.8572 s.

This is the stronger and more paper-significant p=5 empirical event because Aung's own holistic metric says thin bootstrap currently has higher throughput.

## 2. Three value zones for future Step-7 benchmark

Define the active p=5 outcome after correctness/security gates.

### ZONE A — FRONTIER_CROSSING

Conditions:
- candidate satisfies correctness/security/DFR gates;
- T_fast satisfies (T21.1);
- no disqualifying memory/key-size regression that dominates the practical value case.

At unchanged capacity this means:
    T_fast<9.4016 s.

Then:
- p=5 itself becomes a credible empirical value anchor;
- p=5 crosses Aung's published thin-throughput frontier;
- family generalization is useful but not necessary to rescue paper value.

Decision:
    KEEP p=5 ACTIVE through paper completion.

### ZONE B — DIRECT_BASELINE_WIN_ONLY

Conditions:
- candidate passes correctness/security;
- it improves Aung p=5 Corr./TnM latency/capacity;
- but rho_fast<=1 versus thin.

Typical unchanged-capacity interval:
    9.4016 <= T_fast <11.33 s.

Then:
- p=5 establishes that direct RMFE MultKey is a real implementable optimization;
- but it does not move Aung's holistic throughput frontier beyond vanilla thin bootstrap;
- p=5 should remain the CORRECTNESS ANCHOR, not the sole VALUE ANCHOR.

Paper-value requirement:
    at least one higher-k family row must later provide a stronger frontier result,
    OR p=5 must show another material Pareto improvement such as substantially better post capacity at comparable latency.

Preferred later family rows:
    p=3,w=512 for low-risk first replication;
    p=3,w=1024 or p=7,w=1024 for stronger structural leverage.

Decision:
    KEEP p=5 ACTIVE now.
    After its evidence order completes, promote a higher-k generalization only if needed for VALUE.

### ZONE C — NO_DIRECT_VALUE

Conditions:
- T_fast>=11.33 s and C_fast<=101,
or more generally the candidate is Pareto-dominated by the matched Aung p=5 direct baseline on latency/capacity with no compensating key/memory/security gain.

Then:
- p=5 fails its empirical VALUE role;
- the fixed-ring family theorem remains mathematically interesting, but p=5 should no longer consume the main implementation budget.

Decision after evidence-order completion:
    PARK p=5 as implementation anchor;
    reprioritize within the same top-level direct-RMFE-MultKey objective to the first justified family candidate.

AI provisional first pivot:
    p=3,w=512,k=7
because it reuses the same q=5,d_q=8 recovery geometry while eliminating 6 rather than 4 split MultKeys.

This pivot is NOT activated while p=5 Step 2 is pending.

## 3. Capacity-sensitive frontier

Thin-throughput crossing is capacity-sensitive.

Equation (T21.1):

    T_fast <9.4016*(C_fast/101).

Examples:

    C_fast=115:
      threshold =10.7047920792 s.

    C_fast=101:
      threshold =9.4016 s.

    C_fast=90:
      threshold =8.3776633663 s.

Therefore a candidate that spends extra time but materially preserves more capacity can still cross the throughput frontier.

Conversely a fast candidate with large capacity loss may not.

This is why Step 7 must report both latency and post-bootstrap capacity, not speed alone.

## 4. Direct-baseline throughput condition

Against Aung p=5 Corr./TnM itself, with same k:

    throughput_fast / throughput_A
      =(C_fast/101)*(11.3/T_fast).

Thus candidate beats Aung's own throughput iff:

    T_fast <11.3*(C_fast/101).              (T21.2)

At unchanged capacity, essentially any measured latency below 11.3 s improves direct throughput.

But this is weaker than crossing thin.

The review therefore treats:
- direct-baseline throughput win as necessary evidence of useful optimization;
- thin-throughput crossing as the strongest p=5 value event.

## 5. Guarded wrapper must be valued separately

Turn 17's guarded fallback variant has:

    Keys_guarded = Keys_candidate union Keys_baseline

and five live post-projection snapshots.

It may also fallback to the split baseline with probability p_fb.

Therefore the guarded variant cannot be judged by the unguarded T_fast frontier alone.

Let:
    T_shared = Method-1 projection time;
    T_fast_guard = fast tail including certificate overhead;
    T_base = source baseline tail from preserved snapshots.

Conservative expected latency:

    E[T_guarded]
      <=T_shared+T_fast_guard+p_fb*T_base.

For direct latency improvement:

    E[T_guarded] <11.33 s.

For thin-throughput comparison, a branch-dependent post capacity exists.
A conservative guaranteed-capacity comparison uses:

    C_guard,min=min(C_fast,101).

Then a sufficient guarded thin-throughput condition is:

    E[T_guarded]
      <9.4016*(C_guard,min/101).             (T21.3)

A benchmark may additionally report empirical expected throughput using measured branch frequencies, but must define that metric explicitly rather than silently reuse Aung's deterministic-row metric.

The guarded wrapper is therefore primarily a correctness/DFR tool, not automatically the best value variant.

## 6. p=5 remains the cheapest decisive implementation anchor

Reasons NOT to park p=5 now:

1. It is the only row with:
   - exact sparse carrier constants already derived;
   - exact D_j maps/hashes;
   - Turn-8 raw gate;
   - Turn-13 four-output maps;
   - Turn-15/16 canonical correctness machinery;
   - an authorized pending native canary.

2. It has the smallest currently mature implementation surface.

3. It still has a nonempty objective value window:
   ideal T_ideal=7.5444 s versus thin threshold9.4016 s at C=101 leaves1.8572 s for all recovery/guard overhead before the thin frontier is lost.

4. Even if it lands in Zone B rather than Zone A, it provides the correctness proof-of-concept needed before spending native resources on higher-k family rows.

Thus:
    p=5 remains ACTIVE.

## 7. p=5 should not carry the whole paper-value burden by default

Reasons not to overcommit to p=5 as final value anchor:

1. Its absolute idealized end-to-end speedup ceiling is only about1.50x.

2. Its idealized unchanged-capacity throughput ceiling over thin is only about1.246x.

3. The new recovery machinery has nonzero:
   - 10 RM-clear stages;
   - 7 nonidentity Frobenius/key switches;
   - 32 public constant multiplications;
   - 28 additions;
   - cleanups;
   - optional certificate overhead.

4. Guarded mode retains baseline key resources and snapshots.

5. Turn 20 shows stronger structural leverage exists at higher k.

Therefore:
    the final paper should be framed around the FIXED-RING CARRIER FAMILY,
    with p=5 as the first correctness/reference implementation,
    not as "one p=5 optimization."

This is a framing recommendation, not a claim that higher-k performance will win.

## 8. Family escalation rule

After p=5 reaches Step 7:

### If Zone A:
No mandatory family benchmark is required for paper value.
A second row is desirable for generality.

### If Zone B:
One higher-k family benchmark becomes mandatory for a strong algorithmic-value claim.

Preferred sequence:
    first p=3,w=512,k=7
because it reuses q=5,d_q=8 geometry;

if that still does not move a meaningful frontier:
    p=3,w=1024,k=13
or
    p=7,w=1024,k=21.

### If Zone C:
p=5 should be PARKED after its evidence is archived.
The family objective remains alive.
Promote p=3,w=512 as the lowest-regret next active candidate.

No such promotion occurs now.

## 9. Kill / park criteria for the whole family

The family should not be kept alive indefinitely merely because the theorem is elegant.

After at least:
- the p=5 matched value test;
and, if p=5 is Zone B/C,
- one justified higher-k matched value test,

PARK the family if:
- no tested row beats its direct RMFE baseline on a meaningful latency/capacity/resource frontier;
- recovery/certificate overhead scales enough to erase the saved MultKey work;
- or union-key/snapshot costs dominate the claimed practical advantage with no compensating throughput gain.

This prevents the family theorem from becoming a reason to avoid a negative value result.

## 10. VALUE_REVIEW decision

Current evidence says:

IMPORTANT_PROBLEM:
    YES.

CREDIBLE_MECHANISM:
    YES.

P5_PAPER_ANCHOR:
    YES as correctness/reference anchor.

P5_FINAL_VALUE_ANCHOR:
    CONDITIONAL.

FAMILY_VALUE_OPTION:
    CREDIBLE.

IMMEDIATE_PIVOT:
    NO.

PARK_ACTIVE_CANDIDATE:
    NO.

VALUE_GATE:
    remains PENDING.

Why:
- no matched benchmark exists;
- the p=5 value window is nonempty and objectively meaningful;
- the family theorem creates a rational escalation path if p=5 does not cross the strongest frontier.

This is the correct low-regret decision while Step 2 remains pending.

## Verdict

PASS_VALUE_REVIEW.
PASS_P5_REMAINS_CREDIBLE_CORRECTNESS_ANCHOR.
PASS_OBJECTIVE_ZONE_A_B_C_VALUE_POLICY.
PASS_FAMILY_ESCALATION_RULE.
NO_IMMEDIATE_PIVOT.
NO_PARK.

VALUE_REVIEW_COMPLETED=true.

NATIVE_STEP2_RESULT=UNKNOWN / PENDING.
CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
NOVELTY_STATUS=PREFLIGHT.
PAPER_READINESS=NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise do not spend another turn re-evaluating p=5 paper worthiness.
The next side unit should attack a different paper-level uncertainty, preferably:
- independent-style prior-art stress test focused specifically on the fixed-ring carrier theorem; or
- a security/key-footprint pre-audit for the union evaluation-key set.

No benchmark.
No generalization native work.
