# 密码学 17.0 handoff

Resume research — Session Handoff

You are continuing the SAME BOOT research program in the successor conversation 密码学 17.0. This is a session-boundary handoff, not a new research topic.

1. Fixed research identity
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PREVIOUS_SESSION: 密码学 16.0
LATEST_COMPLETED: Research Turn 25/25 — public-artifact Frobenius keyset reproducibility gate
NEXT_ITERATION: successor-session Research Turn 1 / choose next cheapest decisive test
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE / SUCCESSOR_SESSION_CONTINUES_AUTONOMOUSLY
CONTINUOUS_AUTONOMOUS_RESEARCH: true
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
PENDING_PI_DECISIONS: none
RESEARCH_FRONTIER_EXHAUSTED: false

The previous session has exhausted substantive turns 1–25. Turn 26 was HANDOFF ONLY. Do not reinterpret the successor session as Turn 26; it starts a fresh session-local research-turn budget while preserving the same BOOT track/subline.

2. Durable authority / checkpoint

The read-before-write Git checkpoint for the completed session succeeded at:

BBBINGW/memory main@e2bce55cad61755c6ddab1ee2bb7e96679da257e

Treat this checkpoint as the authoritative BOOT session handoff state.

The user-supplied local-Git fallback before handoff had:

HEAD == origin/main @ 87b14e760bf6d6424831d4e44ecfdaf40eea9c4c

but the handoff checkpoint supersedes it.

GitHub Notes was unhealthy during late-session turns. Do not claim connector-derived facts for those turns unless independently reverified. Prefer the verified local Git authority when available.

3. Research philosophy / operating rules

Use the repository philosophy:

smallest falsifiable claim → cheapest decisive test → minimal verification → expand only if warranted

The objective is “填洞式科研”:

first establish a real gap/obstruction;
falsify before optimizing;
distinguish structural contribution from bookkeeping or implementation artifacts;
compare against an exact baseline;
evaluate latency, throughput, key size, memory, ciphertext size, noise/capacity, key-switch count, security assumptions, etc.;
do not treat “nobody seems to have done X” as sufficient novelty;
failed candidates/families should be parked/killed and followed by autonomous in-scope reprioritization;
reversible AI_PROVISIONAL_CHOICE values are advisory, never final PI approval.

Candidate/family substantive-turn budgets remain:

soft budget: 8
hard budget: 12

WAIT_PI or STOP is allowed only when the top-level BOOT research frontier is actually exhausted and must explicitly state research_frontier_exhausted: true.

4. Main surviving candidate

The strongest surviving BOOT candidate is the carry-compensated post-raw RMFE fusion:

keep the five branch-local S2C / reLinearize(recryptKeyID) / rawModSwitch operations;
after branchwise raw switching, aggregate the two public raw channels with exact carry compensation;
reconstruct only once with the common recryptEkey;
run RM10;
exploit the restricted rank-5 post-RM10 subspace;
jointly synthesize the R8 C2S + four correction outputs using five Frobenius terms, i.e. identity plus four nonidentity terms.

Current structural transform count:

75 baseline transform/automorphism terms → 19 candidate terms

This is not yet proven to be 75 → 19 physical key switches.

The candidate remains:

correctness-surviving under current static gates;
latency unresolved;
whole-pipeline capacity unresolved;
publishable novelty not established.
5. Key completed results from 密码学 16.0
Turn 18 — recrypt-key handle / exact linear form

Result:

PASS_STATIC_RECRYPTKEY_HANDLE_LINEAR_FORM

After reLinearize(recryptKeyID), every branch is exactly in basis:

(ONE, BASE(recryptKeyID))

with no branch-specific powerOfX secret handle remaining.

rawModSwitch produces two typed channels corresponding to:

z0 + s_R z1

Envelope shift Y^i, with Y=X^1024, must be public ring multiplication, never automorph/`smartAutomorph`.

Post-raw aggregation/carry correction must keep channel 0 and channel 1 separate.

Single reconstruction with one recryptEkey is exact at CtxtPart/secret-handle level:

Rec(A,B) = Σ_i Y^i Rec(a_i,b_i)

Output basis is (ONE, BASE(0)).

Finding previously persisted at:
findings/boot-RMFE-recryptkey-handle-linear-form-gate-2026-10-31.md

Earlier commit:
817f83578b153fa7010aa3d4c9851f4d1d389390

Turn 19 — recryptEkey noise/intFactor bookkeeping

Result:

PASS_STATIC_RECONSTRUCTION_BOOKKEEPING_DOMINANCE

For the reconstruction boundary:

noise_fused <= noise_five_separate_shifted_sum

with identical:

intFactor
ptxtSpace
primeSet

Therefore the 5→1 recryptEkey fusion introduces no hidden reconstruction-specific HElib BGV capacity penalty.

New implementation invariant:
before HElib ZZX constant APIs, aggregate A,B must be exact negacyclic representatives with

deg(A), deg(B) < 16384

using:

X^16384 = -1

Otherwise embeddingLargestCoeff can fail on unreduced high-degree polynomials.

Finding:
findings/boot-RMFE-recryptekey-noise-intfactor-bookkeeping-gate-2026-11-01.md

Earlier commit:
af6dc182dde1c941c56d8a38b5cfac6a50512aa0

Turn 20 — normalization / DigitExtract boundary

Result:

FAIL_DEFER_NORMALIZATION_THROUGH_DIGITEXTRACT

RM10 normalization:
399 = 2^10 mod 625
224 = 399^-1 mod 625

Normalization can commute through the joint linear recovery, but cannot commute through nonlinear DigitExtract.

Exhaustive check over all 625 residues showed a stronger impossibility:
the unnormalized extracted digit alone does not determine the correctly normalized digit; therefore no output-only correction function exists.

Latest safe point for multiplying by 224:
immediately before DigitExtract

So:

intFactor=399 is not required during joint recovery;
it is required inside the current DigitExtract path.

Staged finding:
boot-RMFE-rm10-normalization-digitextract-boundary-gate-2026-11-01.md
SHA256:
1169fc91a50ce0bcdd85fa3cbfea836c45133afe2a4deed452118ab6b3ce9c52

Evidence:
boot-RMFE-rm10-normalization-digitextract-exhaustive-2026-11-01.json
SHA256:
1093b4acb1ffde1cc94ceb4860f70120dd17a46b506293aab44162035c3b6c7b

Turn 21 — factor-399 capacity transfer

Result:

FAIL_STATIC_DIGITEXTRACT_FACTOR_NEUTRALITY

Do not assume stock factor-1 DigitExtract capacity transfers unchanged to intFactor=399.

However this turn's broad concern was refined substantially by Turn 22.

Staged finding:
boot-RMFE-digitextract-intfactor399-capacity-transfer-gate-2026-11-01.md
SHA256:
2d591fd4080be8b24ffb4e35c0c0901afc6b05b0884e019791f98e272374f1d7

Evidence SHA256:
682785ab523fbf051ccd4891c9edbfee1291b3eb78ac9a9d4ea2afcd23b5648f

Turn 22 — p=5 lifting-polynomial localization

Result:

FAIL_INHERENT_LIFT_FACTOR_HARMONIZATION

For balanced p=5 digits, exact lifting polynomial:

F5(X) = X^5 - 5X^3 + 5X

with factorization:

F5(X) = X * ( X^2 * (X^2 - 5) + 5 )

It admits a 3 ciphertext-multiplication, zero ciphertext-addition schedule, so nontrivial factor harmonization is not inherently required inside each lifting-polynomial evaluation.

Remaining factor risk localizes to the six y-u subtraction / divideByP boundaries.

For e=4:

3 boundaries at plaintext space 625
2 at 125
1 at 25

Maximum sequential dependency depth is 3, not 6.

The old 10.4486764 bits figure is only a generic worst-case pathwise envelope, not a predicted candidate-vs-stock capacity loss.

Staged finding SHA256:
803ee8271c760f7d8c7beb93b1e3f59ec0e8220abb256dff12ed5b2ec26e30de

Evidence SHA256:
0bd064cd1ecf7a7976a1a3056e2ddc554d530c4bd2883050684782fddb2477f7

Turn 23 — six-boundary factor recurrence non-closure

Result:

FAIL_STATIC_SIX_BOUNDARY_FACTOR_RECURRENCE_CLOSURE

At fixed first-boundary prime residue:

q = Q mod 625

the factor-ratio formula is:

rho(f,q) = (f*q)^4 mod 625

For baseline factor 1:
rho_base = q^4

For factor 399:
rho_candidate = 276*q^4

Exact witnesses show the sign is runtime-state dependent:

q=1: baseline aligned, candidate not aligned
q=224: candidate aligned, baseline not aligned

Therefore there is no universal positive factor-399 capacity penalty.

After the first subtraction, HElib's chosen harmonization also depends on actual noiseBounds, and divideByP changes the plaintext space. Static refinement beyond this point is low-value.

Park this branch until actual instrumentation.

Minimal future instrumentation points are only the six y-u / divideByP boundaries, recording:

ptxtSpace
primeSet
Q mod ptxtSpace
intFactor
noiseBound
capacity
harmonization/mod-up events

Staged finding SHA256:
ceb7f8d8842ebfbcec81ca1233694df9462be0f27138a47281ca4f83e406edfe

Evidence SHA256:
62d499714035d4354b070400f8fad4d6718a509d96e167db39d1a455285802f7

Turn 24 — joint recovery Frobenius key coverage

Result:

PASS_FROBENIUS_FAMILY_COMPATIBILITY
FAIL_UNCONDITIONAL_FOUR_KEYSWITCH_COST_CLAIM

Turn 8's reduced-domain support:

{1,5,25,29,17} mod 32

corresponds canonically to full HElib Frobenius powers:

j=0,1,2,3,4

with full-ring exponents:

{1,5,25,125,625} mod 32768

Important implementation invariant:
do not silently interpret reduced labels 29,17 as the full-ring automorphisms for sigma^3,sigma^4.

Canonical implementation should use:
frobeniusAutomorph(j) for j=0..4.

Five automorphism terms / four nonidentity terms remain proven.

But:
4 nonidentity terms != unconditionally 4 physical key switches

because smartAutomorph may use multi-hop key-switch paths unless direct matrices exist.

Staged finding SHA256:
3ff84b4c58f1726e75331947ba56fdc51c3d328ed1948038bfc8a4bde9d6a38f

Turn 25 — public-artifact Frobenius keyset reproducibility

Result:

PUBLIC_ARTIFACT_KEYSET_PROVENANCE_INCOMPLETE

Public Aung et al. artifacts do not establish which exact HElib Frobenius/key-switch matrix-generation strategy was used in the reported p=5,w=512 benchmark.

Established:

joint recovery uses the same Frobenius family as Aung's recode;
required nonidentity powers are j={1,2,3,4};
BSGS execution structurally requires those powers to be reachable/evaluable.

Not established from public artifacts:

direct one-hop matrices for all four targets;
exactly four physical key-switch hops;
zero additional evaluation-key bytes.

HElib addFrbMatrices would be sufficient for direct full-family coverage, but there is no evidence the reported benchmark used that exact configuration.

Therefore retain:

75 -> 19 transform/automorphism terms

Do not currently write:

75 -> 19 physical key switches

Minimal closure audit:
for j in {1,2,3,4}:

target 5^j mod 32768
direct matrix present?
reachable?
actual smartAutomorph hop count?
exact matrices traversed?
stock evaluation-key bytes?
bytes after adding missing direct matrices?

Staged detailed finding:
boot-RMFE-public-artifact-frobenius-keyset-reproducibility-gate-2026-11-01.md
SHA256:
5593ecf086c280849e600f3d7b2dc0665829bfdd7d2023aa9d161545f9c1b0a3

Evidence:
boot-RMFE-public-artifact-frobenius-keyset-evidence-2026-11-01.json
SHA256:
55a28cfd8b76d954b3e62e62434bd917392f9bed12c44bff0846848213cb4ab8

6. Earlier essential BOOT results carried forward

Do not redo these unless a new result directly invalidates their assumptions.

Post-raw fusion

Turn 2:
PASS_STATIC_POST_RAW_SINGLE_BOOTKEY_FUSION

After branchwise rawModSwitch/divisibility handling:
A = Σ Y^i a_i
B = Σ Y^i b_i
and one common boot-key reconstruction:
C = A + B*K

is algebraically equivalent to five separate reconstructions.

Carry theorem

Turns 11–12:

exact post-raw divisibility/carry correction exists;
compact carry state is possible;
aggregate-only fusion before raw rounding is impossible in general;
fusion boundary remains after branchwise rawModSwitch.
Raw work compression limitation

Turn 13:
FAIL_COMPACT_CARRY_TO_COLLAPSE_DOMINANT_RAW_WORK

The current source/dataflow still requires branch-specific toPoly/rounding work because carry decisions depend on branch values.

Therefore raw-side work does not collapse to one branch merely because carry state is compact.

Revised latency/capacity

Turn 15:
PASS_NO_STATIC_CAPACITY_KILL

Capacity-only hard kill:
C_final <= 69.845944

No current static evidence proves such a low ceiling.

Turn 14/15 conclusion:
latency and capacity must eventually be judged jointly.

intFactor correctness

Turn 16:
PASS_STATIC_INTFACTOR_DOWNSTREAM_SEMANTICS

RM10 unit normalization by 224 is semantically valid.
At ptxtSpace 625:
intFactor 1 -> 399

Final HElib restoration rule is:
current_intFactor *= saved_input_intFactor mod application ptxtSpace

Do not manually reset intFactor to the saved input factor.

Restricted joint recovery

Turn 8:
PASS_EXACT_JOINT_C2S_CORRECTION_SYNTHESIS

Restricted post-RM10 rank-5 domain permits exact joint R8 C2S + four correction outputs with:

5 automorphism terms total
identity + 4 nonidentity terms
support represented in reduced R8 domain by {1,5,17,25,29}
4 nonidentity terms are minimal in the established automorphism-multiplier family.

Worst public-multiplier tax:
15.740880 bits

This excludes key-switch noise and is not a whole-pipeline capacity prediction.

7. Killed / parked routes

Keep these closed unless a genuinely new reopening condition appears:

direct pre-raw full-path fusion: killed by nonlinear/raw-rounding obstruction;
generic full-R8 direct four-output map: structurally more expensive than restricted rank-5 map;
one-part dummy reconstruction surrogate: invalid; stock raw path requires two channels;
using Galois automorphism for Y^i envelope shifts: forbidden; it changes secret handle powerOfX;
simple deferral of RM10 normalization across DigitExtract: killed exactly;
output-only correction after unnormalized DigitExtract: killed exhaustively over all 625 residues;
assuming intFactor=399 has a universal positive capacity penalty: false;
further speculative static factor-ledger refinement after Turn 23: park; runtime-state dependent;
claiming 75→19 physical key switches before key-map closure: forbidden;
cross-branch stock hoisting of unrelated ciphertext automorphisms: previously failed;
RMFE high-level “one linear phase” novelty by itself: killed by prior art; any novelty must be in the specific obstruction-aware post-rounding / carry-compensated / restricted-recovery mechanism.
8. Current scientific status

Strongest surviving scientific story:

branchwise unavoidable nonlinear/raw boundary
→ exact public carry compensation
→ 5→1 common recryptEkey reconstruction
→ RM10
→ restricted rank-5 joint Frobenius recovery

This has produced genuine structural understanding:

fusion is blocked before rounding but becomes exact immediately after branchwise raw rounding with public carry state;
common recryptEkey reconstruction is exact and locally capacity-nondominating;
the restricted post-RM10 image dramatically lowers the linear recovery term count;
the remaining performance/capacity questions are concrete implementation-state questions rather than unresolved algebraic correctness.

However:

PUBLISHABLE_NOVELTY: NOT ESTABLISHED

Do not overclaim paper-level novelty until latency, whole-pipeline capacity, and exact prior-art boundary are closed.

9. Next cheapest decisive test in successor session

At successor-session start, first check whether the pending native task result has been delivered.

If the pending native result is available

It preempts the next free substantive turn.

Independently audit:

provenance;
binary/source identity;
timer instrumentation;
warmup/repetition protocol;
exact source-faithful p=5,r=1,m=32768,w=512,k=5 configuration;
timing decomposition;
whether old Turn-4 kill thresholds are obsolete after Turns 11–25;
revised latency/capacity frontier.

Do not rerun the task.

If the pending native result is still unavailable

Choose one highest-EIG independent no-heavy-native unit.

Preferred current candidates:

Key-map closure if accessible from source/config

locate actual key-generation code/config for Aung's benchmark or an exact source-faithful reproduction;
inspect direct matrices/reachability/hop count for j=1..4;
quantify evaluation-key byte tradeoff;
no full benchmark required.

Novelty/prior-art boundary audit
Focus specifically on the mechanism:
branchwise raw-rounding obstruction -> compact public carry correction -> single common boot-key reconstruction -> restricted rank-5 joint Frobenius recovery
Do not search generic “one linear phase” novelty again; that high-level direction is already known.

Reproducibility/candidate instrumentation design
If exact key-map source remains unavailable, prepare the minimal future candidate instrumentation contract:

6 DigitExtract y-u/divideByP points;
4 joint-recovery Frobenius key-map/hop points;
reconstruction degree/negacyclic-reduction assertions;
without starting a second heavy native task.

Do not spend another turn refining speculative intFactor arithmetic without actual prime-set/noise state.

10. Pending Codex/native task — durable provenance

This task remains background work and may cross Research GPT session boundaries.

It must not be restarted, duplicated, replaced, modified, or treated as completed until the orchestrator delivers an actual result.

YAML
task_id: BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01
origin_session_id: 35190a39-0d31-45aa-b03e-33176a25fe96
origin_session: 密码学 16.0
origin_turn: 5
working_directory: /Users/bingwu/Developer/research-orchestrator
execution_backend: Codex CLI / codex exec
model: gpt-5.6-sol
reasoning: medium
pid_or_remote_execution_identity: "691"
start_time: 2026-10-31T11:39:20.875Z
current_status: RUNNING
expected_artifacts: []
evidence_status: PENDING
audit_status: PENDING
result_delivered: false
do_not_rerun: true
commit: null
durable_evidence_reference: orchestrator.db codex_tasks.task_id=BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01

original_hypothesis as preserved in the orchestrator transport:

纯文本
TASK_ID: BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01
Research Turn 5/25 — R8 direct multi-output recovery gate

本轮检验的是：能否把

R8 C2S → unpack → CtxtsToSlots

直接融合成一个更便宜的 R8 → RMFE 线性恢复图。

关键发现：真实接口是 4-output，不是 1-output。

这里 625 = 5^4，所以 correction-style digit extraction 需要：
L0(z)=z, L1(z), L2(z), L3(z).

Aung 的 CtxtsToSlots 正是从五个 scalar branches 通过常数乘法 + 加法同时生成主 ciphertext 和这些 correction images。

因此之前可能想到的“一个 fused map 只需 6 次 automorphism”是不完整的：真实 candidate 必须生成 4 个不同线性输出。

Direct map 存在，但 generic cost 不占优。

每个复合映射 Dt:R8→R, t=0,1,2,3 都是 S=Z/625Z-linear。
利用有限 ring-Galois extension 的标准 automorphism-multiplier 表示，每个 Dt 可以写成 automorphism-multiplier sum。

generic four-output schedule gives 15 automorphism/key-switch terms, while conservative recovery had 13, so generic direct map did not win.

[original_hypothesis truncated for ChatGPT transport; full value remains in orchestrator.db]

The task later became the source-faithful baseline timer decomposition that remains pending. Its result status is still UNKNOWN.

Cross-session rule:

do not wait for this task before doing independent research;
do not reserve a local turn for it;
when orchestrator delivers the result, it preempts the next free substantive turn in the latest active session;
independently audit the result before accepting it;
never infer completion from elapsed time.
11. PI / authorization rules

CONTINUOUS_AUTONOMOUS_RESEARCH remains enabled.

The successor does not need per-iteration PI authorization for:

reversible static analysis;
literature search;
mathematical derivation;
source audit;
cheap non-native falsification;
authorized cheapest-decisive Codex execution when the local slot is free.

However, while the existing Codex/native task is still running, do not start another heavy local native task.

PENDING_PI_DECISION is an advisory durable queue, not automatically blocking.

Rules:

pending PI decision + independent work available → continue no-regret research;
pending PI decision + no independent work available → WAIT_PI;
inheritance by itself is never a reason to WAIT_PI.

Current queue:
none

12. Strict ORCHESTRATOR_CONTROL protocol

Every normal substantive answer in the successor conversation must end with exactly one valid control block:

纯文本
<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

Rules:

CONTINUE

Use when:

autonomous independent research remains;
no immediate delegated execution is being launched;
especially while the existing local Codex slot remains occupied.
EXECUTE

Use only when starting an authorized concrete execution.

Then include:

纯文本
task_id: <explicitly established task identifier>

inside the block.

Never invent a task ID.

WAIT_PI

Allowed only if:

a real PI decision is required; and
no useful independent no-regret work remains.

The block must additionally contain:

纯文本
research_frontier_exhausted: true

if the reason is exhausted top-level research frontier.

If requires_pi: true, always include a truthful
independent_research_available: true|false.

STOP

Allowed only when the top-level objective is scientifically exhausted/closed or an unrecoverable blocker requires stopping.

Must include:

纯文本
research_frontier_exhausted: true

when stopping because the research frontier is exhausted.

Control-only repairs

If the orchestrator asks for a control-block repair:

do not redo research;
do not add claims;
output only the requested control block.
13. Session-start checklist for 密码学 17.0
Restore BBBINGW/memory main@e2bce55cad61755c6ddab1ee2bb7e96679da257e.
Confirm TRACK_ID=BOOT.
Confirm ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS.
Confirm prior session latest completed = Turn 25/25 public-artifact Frobenius keyset reproducibility gate.
Check whether pending task BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01 has a delivered result.
If delivered, audit it first.
If not delivered, select one cheapest decisive independent BOOT test.
Do not rerun or touch the pending task.
Do not reopen parked/killed branches without a new reopening condition.
Keep claims separated into:
proven structural facts;
conditional implementation claims;
unresolved native/capacity/novelty questions.
