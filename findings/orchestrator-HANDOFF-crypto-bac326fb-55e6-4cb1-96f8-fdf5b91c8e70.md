# 密码学 21.0 handoff

Resume research — Session Handoff

This is the successor to completed ordinary-Chat research session 密码学 20.0. It is the SAME logical BOOT research program, not a new topic.

0. Identity / runtime contract
Research role: FHE Bootstrapping Research Student; human is PI and makes final strategic/publication judgments.
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CONTINUOUS_AUTONOMOUS_RESEARCH: enabled.
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false.
Authorized cheapest-decisive Codex execution does not require per-task PI approval.
Candidate soft/hard substantive-turn budgets: 8 / 12.
Failed candidates/families must be KILLed or PARKed and followed by autonomous in-scope reprioritization.
Do not silently change TRACK_ID / ACTIVE_SUBLINE.
The stale root STATE.md CGS target must NOT override this explicit BOOT handoff.
1. Durable authority / checkpoint

GitHub Notes was not healthy during the session. The verified local BBBINGW/memory clone was the durable authority.

Read-before-write checkpoint succeeded at:

3ae9117f958b13abdd11980ed34e463a3636ec69

Treat that commit as the authoritative session checkpoint.

Previous relevant checkpoint before this session's later work:
1e7695d5f8a97fdf10c50ad9427c9cbae3950634.

Do not claim connector-derived writes/facts unless connector health is independently re-established. Prefer verified local Git authority when available.

No new artifact SHA256 values were supplied for Turns 8–25. Do not invent hashes.

2. Session state
LATEST_COMPLETED: Research Turn 25/25 — BOOT frontier-completeness / placement theorem audit
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE
NEXT_ITERATION: resume from this handoff and choose ONE next cheapest decisive BOOT test.
PENDING_PI_DECISIONS: none.
PENDING_PI_DECISION is advisory, not automatically blocking.
If a future PI decision is pending but independent low-regret research remains, continue.
WAIT_PI is allowed only if the entire top-level BOOT research frontier is exhausted; in that case declare research_frontier_exhausted: true.
3. Frozen concrete Aung/HElib setting

Primary concrete setting used throughout this session:

p = 5
m = 32768
RMFE w = 512
k = 5
HElib r = 1
recryption parameters e = 4, e' = 1
raw bootstrap modulus q = p^e + 1 = 626
optimized temporary plaintext modulus after division: p^(e-e'+r) = 625

Aung Corr./TnM published timing sanity point:

SlotsToCtxts: 2.284 s
MultKey: 4.732 s
CtxtsToSlots: 0.078 s
DigitExtract: 4.240 s
total: 11.334 s
Corr./TnM final capacity about 101
remaining multiplication count about 5

Published thin sanity point:

capacity about 151
remaining multiplication count about 8
latency about 2.82 s

These are external sanity points only; same-machine paired evidence is required for strict systems verdicts.

Preregistered systems-value interpretation retained from prior sessions:

correctness failure preempts all timing interpretation;
strong/value claims require meaningful paired same-machine improvement;
latency improvement below approximately 10% without another strict Pareto gain is not enough for the intended systems contribution.
4. Historical candidate entering this session

The session originally inherited a sparse/power-coordinate candidate:

canonical coordinate set
J={0,1024,7168,2048,6144}
former five-branch sparse packing / shared HElib recryption middle / pruned unpack architecture
canonical pruned unpack count: 17 Frobenius calls
historical transform-side count: candidate 19 versus stock 75
four RMFE correction outputs L0,L1,L2,L3

Turns 8–10 established:

all five scalar leaves are required;
L_t cannot be replaced exactly by successive Frobenius images of L_0;
17 calls are locally optimal in the fixed canonical binary tree;
the theoretical 16-call bit-reordered tree cannot be obtained by a free affine/Frobenius/monomial preconditioner;
cheap 17→16 micro-optimization family is closed.

Those results remain true as local transform facts, BUT the entire sparse/shared-middle ordering was later killed by a more fundamental exact 5-adic correctness obstruction. Do not resurrect it merely because its transform count looked attractive.

5. Key session discovery: prior correctness theorem was too weak

Turn 12 found that the prior statement

selected recovered leaves only need to be correct modulo 5; higher 5-adic digits may be dirty

is FALSE for the actual HElib/Aung digit-extraction interface.

For p=5,e=4,e'=1,r=1, HElib ultimately extracts the digit beginning at position

e-e' = 3,

not merely the residue modulo 5.

Minimal control:
1 and 126 = 1 + 5^3 agree modulo 5 but produce different relevant high digits.

Verdict:
FAIL_MOD5_DIRTY_LIFT_SUFFICIENCY.

This reopened and then killed the inherited static-correctness story.

6. Exact dirty-state obstruction — Turns 13–17
Turn 13

Using the audited local transport

A =
[[1,1],
[443,182]]

and

A^{-1} =
[[313,91],
[313,534]] mod 625,

a valid shared transformed lift can decode correctly before inverse but, after applying the dense inverse, yield branch lifts whose digit-3 values are wrong.

Verdicts:

FAIL_EXACT_Z625_LEAF_EQUIVALENCE_FROM_CURRENT_INVARIANTS
FAIL_DIRTY_LIFT_LINEAR_INVERSE_COMMUTATION
Turn 14

HElib's actual rawModSwitch → newMakeDivisible state model does not provide the hidden canonical-lift invariant needed to exclude those dirty states.

For e'=1:

D(z) = (z + 626 v(z))/5

and, when both values stay centered,

D(z+5)=D(z)+1.

The current sparse-pack/shared-make-divisible/dense-inverse ordering was therefore KILLed.

Verdicts:

PASS_REACHABLE_DIRTY_STATE_COUNTEREXAMPLE
FAIL_SHARED_DIVISIBILITY_THEN_INVERSE_CORRECTNESS
Turn 15

Keeping only public newMakeDivisible residue/carry information at stock plaintext modulus 625 is insufficient.

Example:
z0=-312, z1=313
have the same residue modulo 625 and same make-divisible correction, but after divide their outputs differ by 125.

Verdict:
FAIL_PUBLIC_CARRY_SIDEINFO_REPAIR_WITH_STOCK_RECRYPTEKEY.

A larger 3125 modulus was identified as the natural unoptimized modulus, but remained only a reopening candidate.

Turn 16

Merely raising the boot-key plaintext modulus to 3125 and delaying /5 does NOT repair the killed architecture:

because M(y)=5D(y) and the inverse is linear,

A^{-1} M(y) / 5 = A^{-1} D(y) mod 625.

Verdict:
FAIL_3125_DELAYED_DIVIDE_REPAIR.

Fully deleting newMakeDivisible would be a genuinely different unoptimized family, but current w=512, eta=125 Aung correction parameters cannot simply be reused at an e=5 correction modulus; the source interpolation requirement would become roughly eta >= 625, implying w >= 2501 for k=5.

Turn 17

Even deleting newMakeDivisible entirely does not save the current pack-before-modswitch family.

rawModSwitch itself performs coefficientwise scale/round/center operations, and an explicit counterexample showed

R_Q(Ax) != A R_Q(x)

at exactly the high 5-adic semantics needed by unoptimized digit extraction.

Verdicts:

FAIL_RAWMODSWITCH_LINEAR_COMMUTATION
KILL_UNOPTIMIZED_3125_PACK_BEFORE_RAWMODSWITCH_REPAIR

The nonlinear correctness barrier was therefore located at rawModSwitch itself.

7. Turn 22 structural theorem — balanced-lift rigidity

This is one of the strongest scientific results of the session.

For odd p=2h+1, let

beta : F_p -> {-h,...,h}

be the balanced lift, extended coordinatewise.

Let A in GL_n(F_p) and let Â be its balanced integer lift.

If

beta(Ax) = Â beta(x) in Z^n for every x in F_p^n,

then Â must be a signed permutation matrix.

Proof idea:
for every row a of Â, balanced output for every z in [-h,h]^n forces

max |a·z| = h sum_j |a_j| <= h,

so each row has l1 norm <=1; invertibility forces exactly one ±1 per row/column.

Verdict:
PASS_BALANCED_LIFT_RIGIDITY_THEOREM.

Consequence:
any genuine universal linear branch mixing before centered representative selection necessarily creates carry discrepancy.

8. Turn 23 — theorem applies to actual Aung workload

A possible loophole was that RMFE/Aung messages might occupy only a special code subset.

Turn 23 closed it.

For the actual p=5,k=5 Aung split workload, the five logical branch values at a fixed slot range over the full domain

F_5^5.

RMFE injectivity does not impose a lower-dimensional relation, and branchwise invertible SlotsToCoeff does not remove that freedom.

Verdicts:

PASS_AUNG_WORKLOAD_FULL_F5K
PASS_RIGIDITY_THEOREM_APPLIES_TO_ACTUAL_K5_WORKLOAD

Therefore the rigidity obstruction is application-specific, not merely a theorem about synthetic arbitrary inputs.

9. Turn 24 — information-loss collision

Turn 24 strengthened the obstruction beyond linear inverse failure.

There exist distinct valid pre-modswitch branch states x != x' such that

R_Q(Ax) = R_Q(Ax')

but

R_Q(x) != R_Q(x').

Therefore NO deterministic decoder—linear or nonlinear—can reconstruct exact branchwise raw-modswitched representatives from the shared raw output alone.

Verdicts:

PASS_INFORMATION_LOSS_COLLISION
FAIL_SIDEINFO_FREE_NONLINEAR_REPAIR

This means exact repair requires additional carry/rounding side information.

Important qualification:
raw ciphertext coefficients are public, so a carry-aware scheme could in principle preserve/compute side information before information is lost. The unresolved issue is whether this side information can be obtained substantially cheaper than performing the branch-local transforms whose cost we were trying to avoid.

Surviving opening:
CARRY_AWARE_COEFFICIENT_SIDECHANNEL_OPEN.

10. Turn 25 — make-divisible rigidity and full placement classification

For

M(z)=z-q beta(z mod p),

mixing after rawModSwitch but before newMakeDivisible obeys

M(Âz)-ÂM(z) = q(Â beta(zbar)-beta(A zbar)).

Exact commutation therefore again requires the Turn-22 balanced-lift identity and hence only signed permutations.

New verdict:
KILL_LINEAR_MIX_BETWEEN_RAWMODSWITCH_AND_MAKEDIVISIBLE.

Complete ordinary-linear placement map:

Before / inside SlotsToCoeff
KILLED/PARKED. Genuine mixing eventually crosses rawModSwitch and hits rigidity. Pure cross-ciphertext hoisting was unsupported by stock HElib and previously had only a small ceiling.

After SlotsToCoeff, before rawModSwitch
KILLED by Turn 17 + Turns 22–23.

After rawModSwitch, before newMakeDivisible
KILLED by Turn-25 make-divisible rigidity.

After newMakeDivisible, before /5
No distinct opportunity; once divisible, /5 is linear, so this is equivalent to post-divide sharing.

After /5, before recryptEkey reconstruction
Correct semantics exist, but systems value is weak; see Turns 18–21 below.

After reconstruction, before CoeffToSlots
KILLED/PARKED: full dirty extension-valued states lose branch identity under aggregation, and stock HElib cross-ciphertext hoisting does not share the decomposition.

After CoeffToSlots
Too late; expensive MultKey work is already paid.

Immediately before DigitExtract
Baseline/Aung territory, not a MultKey-sharing solution.

Turn-25 verdict:
PASS_ORDINARY_LINEAR_PLACEMENT_FRONTIER_CLOSED

with:
PASS_MAKEDIVISIBLE_RIGIDITY_COROLLARY.

11. Post-divide sharing candidate — Turns 18–21

After all nonlinear preprocessing is kept branch-local, each branch reconstruction has the form

C_i = b_i E + a_i

for the same encrypted recryption-key ciphertext E and public branch-dependent a_i,b_i.

Turn 18

By linearity, each correction output can be written as an affine linear function of the same E.

Semantic factorization is exact.

Verdicts:

PASS_POSTDIVIDE_COMMON_RECRYPTEKEY_FACTORIZATION
PASS_DIRECT_FOUR_CORRECTION_AFFINE_MAP_SEMANTICS
Turn 19

Directly collapsing all correction maps into generic dynamic ThinEvalMap-like maps destroys the useful stock trace structure and is not attractive.

A narrower r=2 shared-prefix schedule is algebraically legitimate because all automorphisms really start from the same E.

Physical transform-KS count:

stock post-divide tail:
70

r=2 prefix-hoist:
62

including unavoidable branch-local transform calls:
75 -> 67

Verdicts:

PASS_COMMON_RECRYPTEKEY_PREFIX_HOIST
FAIL_DIRECT_FOUR_CORRECTION_GENERIC_MAP_AS_PRIMARY_PATH
VALUE_UNRESOLVED_NEAR_THRESHOLD
Turn 20

Even under extremely favorable accounting—new constant multiplications/additions treated as zero cost and full CtxtsToSlots credited as eliminated—the expected full Corr./TnM latency gain is only roughly 5%, far below the preregistered 10% value target.

Verdict:
FAIL_EXPECTED_VALUE_LATENCY_GATE.

Only a strict capacity/Pareto rescue remained.

Turn 21

HElib noise propagation provides no static theorem that the shared-prefix schedule strictly lowers any output's noise/capacity. Physical KS sharing does not divide inherited noise among outputs, and extra constant multiplications/additions can offset the saved key-switch noise.

No other strict Pareto axis remained.

Verdict:
FAIL_PROVABLE_STRICT_CAPACITY_PARETO.

Final disposition:
PARK_R2_COMMON_RECRYPTEKEY_PREFIX_HOIST.

Do not allocate a standalone native task to this parked candidate. It may only be measured opportunistically if an already-necessary harness happens to expose it cheaply.

12. Prior-art / novelty boundary retained

Aung et al. explicitly identify repeated MultKey on RMFE-split ciphertexts as an open bottleneck. That makes the problem real.

However broad novelty claims are already killed by prior work:

Geelen–Vercauteren ePrint 2024/1587: batching/packing multiple ciphertexts through shared bootstrap work and unpacking before digit removal.
Liang–Ding ePrint 2026/1779: ring switching without slot recovery / independent leaf evaluation. It partially subsumes broad non-restored-representation / partial-coordinate narratives.

Liang–Ding does NOT directly reproduce the now-killed sparse/shared HElib mechanism, but it narrows novelty substantially.

Retain only narrow claims tied to the actual Aung/HElib obstruction; search absence is never novelty proof.

13. Current strongest scientific conclusion

The most important result of 密码学 20.0 is no longer an optimization candidate.

It is this structural boundary:

In the actual Aung p=5,k=5 workload, centered representative selection in HElib preprocessing creates a carry/information barrier. Any nontrivial universal linear branch mixing before or across rawModSwitch/newMakeDivisible fails exact higher-`5`-adic correctness; side-information-free nonlinear decoding also cannot recover the lost branchwise representatives.

Equivalently:

ordinary linear pack-before-modswitch family = CLOSED

under:

stock HElib rawModSwitch;
stock make-divisible optimization;
full actual Aung message domain;
universal exact correctness.

This is stronger than "our matrix happened to fail".

14. Current killed / parked routes

Do NOT reopen without changing a premise.

KILLED:

original sparse-power-coordinate shared-middle architecture;
mod-5-only dirty-lift correctness claim;
shared make-divisible/divide followed by dense inverse;
public make-divisible carry metadata at stock modulus 625;
3125 + same make-divisible + delayed divide;
unoptimized 3125 pack-before-rawModSwitch route;
arbitrary ordinary linear mixing before rawModSwitch;
ordinary linear mixing after rawModSwitch but before make-divisible;
side-information-free nonlinear unmixing;
direct four-correction generic-map path as primary systems candidate;
old aggregate-only dirty-extension fusion;
naïve additive preprocessing without carry;
hidden pre-fusion rank-5 invariant;
RM10-alone / complement / p-divisible complement rescue families;
high-level "single linear phase" novelty;
broad batch/shared-bootstrap novelty;
broad "non-restored representation" novelty.

PARKED:

r=2 common-recryptEkey prefix hoist: semantically valid but insufficient expected value and no provable strict Pareto;
Liang–Ding k=2 late-moddown competitor: unresolved but secondary and not primary;
other old low-value cross-branch hoisting routes.
15. Strongest open family / current frontier

The ordinary-linear placement frontier is closed, but the top-level BOOT frontier is NOT exhausted.

Strongest genuinely open families require changing a premise:

Carry-aware representation / coefficient sidechannel

preserve enough rounding/carry information across rawModSwitch;
Turn 24 proves a decoder from shared output alone is impossible;
key unresolved question: can required carry state be derived substantially cheaper than materializing the five branch-local transforms?

Modified modulus switching

design a rounding/modswitch procedure equivariant under a useful branch-mixing representation.

Different algebraic representation

must avoid the full-domain balanced-lift rigidity; merely choosing another invertible linear matrix is NOT enough.

Different restricted workload/parameter regime

only if the actual branch domain ceases to be full F_p^k or another premise changes materially.
Main unresolved question for the successor

The current highest-value unresolved issue from Turns 24–25 is:

Can the lost coefficientwise carry/rounding information needed for exact branch recovery be computed/preserved from pre-mix public state at cost materially below the five branch-local transforms it is intended to replace?

A falsifier should show that computing this side state requires materializing information equivalent in cost/structure to the branch-local SlotsToCoeff → reLinearize states.

A positive result must give an explicit carry-aware mechanism with concrete operation/storage cost; "carry information exists" is not enough.

Choose ONE smallest falsifiable version of this question as the next iteration. Do not start a heavy native experiment unless a cheap static/source gate first survives.

16. Latest native/Codex evidence — inert, already delivered

The following task provenance MUST be carried exactly as background/inert state. It must NOT be restarted, duplicated, or treated as pending unknown work.

TASK_ID:
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

origin_session_id:
1f28610c-0aa3-4cce-9ec9-158d114c5ae8

origin_session:
密码学 17.0

origin_turn:
4

original_hypothesis:
TASK_ID: BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01 — paired same-machine throughput gate. Compare vanilla thin, source-faithful Aung Corr./TnM, and the then-current post-raw fusion candidate under the same HElib commit/context/keyset/hardware protocol; correctness mismatch must stop performance interpretation. Full original_hypothesis remains in orchestrator.db; the transported text was truncated.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
medium

pid_or_remote_execution_identity:
54891

start_time:
2026-10-31T19:00:21.095Z

current_status:
COMPLETED

expected_artifacts:
[]

artifact_count:
197

evidence_status:
AVAILABLE

audit_status:
DELIVERED

result_delivered:
true

do_not_rerun:
true

commit:
4326551c9825f719414e094935ec1db554f0c6fc

result:
FAIL_NATIVE_CORRECTNESS

Exact interpretation:

vanilla thin correctness PASSED;
source-faithful Aung Corr./TnM failed its first smoke-run correctness check;
contract stopped immediately;
candidate was NOT executed;
NO performance/capacity/CI/throughput verdict exists;
RM10/joint physical-hop audit was never reached;
therefore this result is a comparator implementation/harness blocker, NOT evidence that the later Turn-12–25 scientific conclusions or current carry-aware frontier are false;
the exact 741 MiB keyset was persisted and must be reused if ever needed; do NOT repeat the approximately 5.5-hour key generation.

Evidence:

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-run.log
/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-progress.jsonl
/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/source/benchmark.cpp

Durable evidence reference:
orchestrator.db codex_tasks.task_id=BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

This task is completed/delivered/inert. It remains part of cross-session provenance only. DO NOT restart or duplicate it.

17. Cross-session Codex/native lifecycle rules
Codex/native task lifecycle is independent of Research GPT session lifecycle.
A task may cross session boundaries.
Never infer a result before it is delivered.
Never modify the source/work directory/binary of a task that is running.
Never resubmit/restart/duplicate an existing task.
Never reserve a session-local turn waiting for a task.
If an active task exists, continue independent research and use CONTINUE, not EXECUTE.
When a task result becomes ready, the orchestrator will deliver it to the latest active session; independently audit it on the next free substantive turn.
Completed tasks with do_not_rerun=true remain inert provenance.
New heavy/native work should only be delegated after the cheapest static/source/math falsification gate survives.
An authorized cheapest-decisive Codex task does not require separate PI approval, but task identity/provenance must be explicit.
18. Research philosophy / execution discipline

Follow RESEARCH_PHILOSOPHY.md and AGENT.md.

Default loop:

smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted.

Each substantive research turn:

ONE primary hypothesis;
ONE cheapest decisive test;
clear falsifier;
end with PASS / FAIL / UNCLEAR or KILL / PARK / CONTINUE disposition;
distinguish source fact, mathematical derivation, static model, and native measurement;
do not turn absence of search results into novelty proof;
do not optimize a family already killed by a stronger obstruction;
preserve explicit reopening conditions for parked/killed routes;
PI retains final decision on publication importance and strategic pivots.
19. PI / autonomy rules

Human PI decides:

final direction;
whether a gap is important;
publication value;
acceptable assumptions/trade-offs;
major irreversible pivots.

Agent may autonomously:

continue literature/source audit;
derive/falsify;
PARK/KILL failed candidates;
reprioritize within BOOT;
make reversible AI_PROVISIONAL_CHOICE decisions;
delegate an authorized cheapest-decisive Codex task when justified.

Do not WAIT_PI merely because:

a candidate failed;
a task is pending;
a PI advisory item exists;
the session changed.

WAIT_PI/STOP only when the entire top-level BOOT frontier is genuinely exhausted.

20. Strict ORCHESTRATOR_CONTROL protocol for the successor

Every NORMAL substantive research answer in the new conversation must end with exactly one valid control block:

<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

Additional rules:

independent_research_available should normally be included on every control record and MUST be included whenever requires_pi: true.
If action: EXECUTE, include:
task_id: <explicitly established task identifier>
inside the block.
Never invent a task_id.
While a local/heavy Codex task is active, use CONTINUE, not EXECUTE.
WAIT_PI and STOP are allowed only if the TOP-LEVEL research frontier is exhausted and must additionally include:
research_frontier_exhausted: true
A pending PI advisory queue by itself is not sufficient reason for WAIT_PI.
A HANDOFF-ONLY answer is the exception: it does not use ORCHESTRATOR_CONTROL and must obey the handoff format requested by the controller.
milestone: true should be used for durable major scientific/state transitions (theorem, family kill, session checkpoint, decisive gate); otherwise false.
21. Successor starting point

Do not redo Turns 12–25.

Do not reopen ordinary linear pack-before-modswitch variants unless a premise of the rigidity theorem is explicitly changed.

The next substantive iteration should choose ONE cheapest decisive test from the genuinely open frontier, with priority on the carry-aware question:

Can exact carry/rounding side information be obtained materially cheaper than evaluating the branch-local transforms it is meant to replace?

If that family fails, PARK/KILL it and autonomously reprioritize to another BOOT family such as a genuinely modified modulus-switching rule. Do not WAIT_PI unless the whole BOOT frontier is exhausted.
