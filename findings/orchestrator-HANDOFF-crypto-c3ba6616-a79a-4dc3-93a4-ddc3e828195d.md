# 密码学 13.0 handoff

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED: Research Turn 25/25 — PASS_DECISION_MATRIX_READY / SESSION_CHECKPOINT_READY
NEXT_ITERATION: Independently audit BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-NATIVE-20261029-R23-01 before choosing the next cheapest decisive BOOT step
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE; CONTINUOUS_AUTONOMOUS_RESEARCH; R23 evidence AVAILABLE and audit READY
PENDING_CODEX_TASKS: These are inert provenance records, NOT execution requests.

# Resume research — Session Handoff

This is the successor to the completed ordinary-Chat Research Session 密码学 12.0. It is the SAME logical BOOT research program, not a new topic.0. Required runtime identitySurface: ordinary Chat, NOT Work.Research GPT: gpt-5.6-sol.Reasoning: xhigh / Extra High.Codex when delegated: gpt-5.6-sol / xhigh.ZERO_API_BILLING: YES.Paid/API fallback: FORBIDDEN.Silent model downgrade: FORBIDDEN.Silent reasoning-effort downgrade: FORBIDDEN.If the required model/reasoning is unavailable, stop with the corresponding runtime/model blocker rather than silently downgrading.1. Durable authority / read-before-write checkpointThe read-before-write Git checkpoint for the completed session succeeded at:BBBINGW/memory main@62ba99ff9529bfd54f741796d8b4dbb8b9b57bc5This commit is the durable starting authority for the successor session.Restore state from GitHub first, beginning with:findings/boot-STATE.mdthe latest BOOT handoff/checkpoint finding created at 62ba99ff9529bfd54f741796d8b4dbb8b9b57bc5any finding referenced there for the source-r=1 RMFE one-core candidatepending Codex provenance recordsDo not overwrite this state from older memories or older session summaries.Fixed identity:纯文本TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CONTINUOUS_AUTONOMOUS_RESEARCH: ENABLED
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
PENDING_PI_DECISIONS: none
RESEARCH_FRONTIER_EXHAUSTED: falseB175_DIRECT_SI_POINTWISE remains killed. B158 remains an active redesign program. The currently strongest provisional successor is the source-faithful RMFE fixed-ring one-core construction.2. Completed-session boundaryResearch Turns 1–25 of 密码学 12.0 are complete.Latest completed substantive turn:纯文本Research Turn 25/25
SOURCE_R1_POST_NATIVE_DECISION_MATRIX_AND_SESSION_CHECKPOINT
RESULT:
PASS_DECISION_MATRIX_READY / SESSION_CHECKPOINT_READYThe old session is closed for substantive research.If the pending R23 result is not yet independently audited when this successor starts, that audit PREEMPTS the next free substantive research turn.Do not count the old session's mandatory handoff as a substantive research turn.3. Current scientific candidateThe current paper-lane candidate is source-faithful:纯文本p = 5
r = 1
m = 32768
w = 512
k = 5
eta = 125
normal_basis = falseThe intended chain is:GR(5,512)→E8→one fixed-ring HElib recryption core→E8(mod625)→5 recovered thin coordinates→Aung correction.GR(5,512)
\rightarrow E_8
\rightarrow \text{one fixed-ring HElib recryption core}
\rightarrow E_8 \pmod{625}
\rightarrow 5\text{ recovered thin coordinates}
\rightarrow \text{Aung correction}.GR(5,512)→E8​→one fixed-ring HElib recryption core→E8​(mod625)→5 recovered thin coordinates→Aung correction.This is distinct from the older R21 r=4 stress canary.The source-faithful HElib parameters are:纯文本e = 5
ePrime = 2
q = 5^5 + 1 = 3126
post-core plaintext modulus = 5^(5-2+1) = 625
1024^-1 mod 625 = 2244. Session accomplishments and stable positive evidenceThe following are established independently of the pending native result:纯文本deterministic p=5,w=512 RMFE instance:
PASS_STATIC

consecutive rank-5 -> R8 plaintext interface:
PASS_STATIC

exact R8 S2C/C2S maps:
PASS_STATIC

exact grouped six-KS realization:
PASS_STATIC

source-r=1 modulus/type chain:
PASS_STATIC

e=5,ePrime=2, post-core modulus=625:
PASS_SOURCE

normalization 224 mod625:
PASS

Aung correction eta=125 compatibility:
PASS_STATIC

pre-rawModSwitch capacity ceiling:
STRONG_PASS_STATIC

post-core RM10/C2S layout/noise ceiling:
PASS_STATIC_NO_KILL

hidden HElib multi-hop automorphism inflation:
NONE

candidate middle automorphism KS applications:
29 actual

baseline five-branch automorphism KS applications:
75 actual

including recrypt-key switch:
candidate 30 vs baseline 80

boot-key encrypted-secret core count:
1 vs 5

M < 2.8 s structural plausibility:
PASS_PLAUSIBLE

specific direct prior collision:
NOT_FOUND

abstract/high-level novelty:
substantially killed/down-scopedThe key remaining scientific uncertainty is now concentrated in:纯文本native functional correctness
actual post-middle capacity
actual candidate-middle latency
same-machine split-baseline ratio5. Stable killed / negative claimsThese claims are dead and must NOT be resurrected even if the source-r=1 native gate eventually passes:纯文本five split paths commute exactly through rawModSwitch:
FAIL

generic GR(625,512) -> E8 ring embedding:
FAIL

truncated Aung Algorithm-4 prefix gives r>1 block recovery:
FAIL

one-final-recode Chen-Han at eta=125 for the r=4 generalized lane:
FAIL

old r=4 R21 gate globally decides source-r=1 family:
FAIL

"one linear phase instead of multiple" is itself novel:
FAIL — explicitly disclosed by Aung et al. as future work

generic temporary-envelope/ring-switch philosophy is new:
FAIL — AP13 / Geelen and related prior art

generic component-compression philosophy is new:
FAIL

restricted 5-term J works on arbitrary noncanonical RMFE input:
FAIL

evaluation-key-memory asymptotic advantage:
NOT ESTABLISHED / likely noDo not pitch a “new general envelope theorem” as the primary novelty.The plausible contribution type is instead:fixed-ring HElib algorithmic realization of Aung et al.'s open single-linear-phase direction, with concrete k -> 1 recryption-core compression, reduced automorphism/KS execution, complexity analysis, and experimentally meaningful throughput improvement.6. Complexity result that survived auditFor the current pinned HElib strategy:纯文本baseline middle automorphism KS:
75

candidate middle automorphism KS:
29

reduction:
61.33%

including recrypt-key switch:
80 -> 30
reduction = 62.5%

boot-key core:
5 -> 1The source audit established that these are actual direct KS-matrix applications, not merely requested automorphisms hidden behind multi-hop smartAutomorph() paths.Family-level linear-phase result:Θ(klog⁡d)→O(k+log⁡d)\Theta(k\log d)
\rightarrow
O(k+\log d)Θ(klogd)→O(k+logd)for automorphism/KS complexity, with:k→1k\rightarrow1k→1boot-key/recryption cores.Do NOT claim the entire RMFE bootstrapping algorithm has this asymptotic improvement. DigitExtract/correction remains outside this separation.ct-pt work remains Θ(k)\Theta(k)Θ(k) and may increase in constant factor.Key memory does NOT have a proved asymptotic advantage.7. Performance/value decision matrixUse the Turn-25 checkpoint rules when interpreting any native result.Holistic model:Tcand=6.602+M,T_{\rm cand}=6.602+M,Tcand​=6.602+M,where M is candidate middle latency.Candidate throughput:TP(C,M)=10C6.602+M.TP(C,M)=\frac{10C}{6.602+M}.TP(C,M)=6.602+M10C​.Thin baseline throughput:纯文本107.06Beat-thin condition:C>10.706(6.602+M).C > 10.706(6.602+M).C>10.706(6.602+M).Useful checkpoints:纯文本M = 2.0 s -> required final C > 92.09
M = 2.5 s -> required final C > 97.45
M = 2.8 s -> required final C > 100.66
M = 3.0 s -> required final C > 102.80
M = 3.5 s -> required final C > 108.15
M = 4.0 s -> required final C > 113.51
M = 4.5 s -> required final C > 118.86
M = 4.732 s -> required final C > 121.34Absolute final-capacity value kill floor:C≤70.68C\le70.68C≤70.68means the candidate cannot beat thin even if M=0.Promotion guidance:纯文本M < 2.0 s + healthy capacity:
STRONG_PROMOTE

2.0 <= M < 2.8 s + correctness PASS:
PROMOTE_TO_FULL_CORRECTION_BENCHMARK

2.8 <= M < 4.5 s:
CONDITIONAL — promote only if capacity is unusually strong

M >= 4.5 s:
PARK as low-value engineering result unless capacity is exceptionalSame-machine middle speedup interpretation:纯文本S_middle < 1.3:
weak systems value

1.3 <= S_middle < 1.7:
useful engineering

1.7 <= S_middle < 2.0:
credible research signal

S_middle >= 2.0:
strong mechanism evidenceStrong internal paper target:纯文本>= 1.10x thin throughput8. Native-result decision matrixFor the source-r=1 R23 gate:纯文本SOURCE_BLOCKED before keygen:
no mechanism evidence
fix source provenance only; do not kill

UNCLEAR / instrumentation failure before encryption:
no mechanism evidence
repair instrumentation; HUMAN_REVIEW if repeated

context/security mismatch:
PARK current fixed instantiation

projection oracle FAIL:
localize source/interface issue; not immediate family kill

envelope/S2C linear oracle FAIL:
custom implementation failure; not immediate algebraic family kill

pre-raw capacity FAIL:
PARK fixed candidate and inspect attribution

rawModSwitch bound FAIL:
FAIL fixed source-r=1 instantiation

newMakeDivisible congruence/divisibility FAIL:
likely source/harness issue -> HUMAN_REVIEW

RM10/C2S/unpack linear oracle FAIL:
post-core implementation failure

all prior oracles PASS + scalar extractDigitsThin FAIL:
DECISIVE SCIENTIFIC FAIL of one-core p-adic semantics
KILL/PARK current source-r=1 one-core mechanism

canonical PASS + noncanonical FAIL:
kill general Aung claim
retain canonical fast path only

correctness PASS + nonpositive retained capacity:
KILL fixed parameter candidate

correctness PASS + healthy capacity + useful timing:
PROMOTEThe most important decisive scientific FAIL condition is:纯文本all custom linear/raw invariants PASS
AND
native scalar extractDigitsThin oracle FAILSbecause that localizes the failure to the one-core p-adic premise rather than a map/harness issue.9. Old R21 result is CLOSED, not pendingOld task:BOOT-RMFE-P5W512-CONSECUTIVE-R8-MERGED-MIDDLE-FIXEDQ-NATIVE-20261029-R21-RECOVERY-01was independently audited in 密码学 12.0 as:纯文本PARTIAL_EXECUTION_DETECTED
SCIENTIFIC_RESULT = UNCLEAR
DO_NOT_RERUN = trueIt stopped before encryption because of a recrypt-key-ID instrumentation mismatch.Pinned HElib source showed that private-layout introspection is unsafe. Future harnesses should use:SecKey::genRecryptData() return value as authoritative recryptKeyID;public PubKey::writeToJSON() to read serialized recryptKeyID and recryptEkey;public Ctxt::readFromJSON() to reconstruct recryptEkey.R21 is CLOSED and must not be restarted, resumed, modified, or treated as the current experiment.10. Current R23 Codex/native evidence — HIGH PRIORITY AUDIT FIRSTThe current task is:BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-NATIVE-20261029-R23-01The orchestrator now reports that this task is COMPLETED, evidence is AVAILABLE, audit status is READY, and result has NOT yet been delivered/accepted by Research GPT.Reported Codex classification:纯文本SOURCE_BLOCKEDReported stopping point:fresh static preflight stopped at the grouped-S2C canonical hash check, exit code 2.Before that, Codex reports:纯文本R14/R16/R17/R18 ZIP outer hashes:
PASS

internal hashes:
PASS

R18 exact two-slot identity reverification:
exit 0

tau_i(phi(e_j)) mod625:
25/25 PASS

tau_i(phi(e_j)) mod5:
25/25 PASSNo HElib build/context/key/encryption/native candidate stage/raw invariant/DigitExtract/timing ran.Reported artifact:纯文本/Users/bingwu/Developer/research-orchestrator/
BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-NATIVE-20261029-R23-01.zip

bytes:
103976

SHA-256:
c9c563be6a9e3e2a646822e55813d5e5048c229ed57116988bd40595dd7592f0

internal SHA256SUMS:
37 files, all reportedly verified

ZIP integrity:
PASSGit reportedly remained:纯文本bb9e5d3413e75362c0f26f29bd3ec4d9bf64e11cwith tracked and pinned-HElib diffs empty.No commit or research-memory write was made by that scientific task.Mandatory successor actionThis R23 evidence MUST be independently audited on the successor's next free substantive turn before any scientific acceptance.Likely scope:verify whether the grouped-S2C canonical hash check is valid for the source-r=1 mod-5 reduction;determine whether the hash mismatch is a real source prerequisite failure or an over-constrained preflight artifact inherited from mod-625/R14 lineage;verify artifact provenance/hashes where accessible;classify PASS / FAIL / UNCLEAR / HUMAN_REVIEW at exact scope;do NOT rerun the same R23 task.Because the reported task stopped before native scientific execution, a confirmed preflight/hash-only blockage would NOT be a scientific FAIL of the candidate.11. Parked r>1 Chen–Han side familyCurrent status:纯文本Aung-prefix truncation:
FAIL

direct one-final-recode Chen–Han at eta125:
FAIL

standard Chen–Han with two recodes:
PASS_STATIC

novelty:
high-level direction already disclosed

status:
PARK_AS_VALID_REOPENING_MECHANISMCopy for WordDo not return here unless the source-r=1 one-core line first produces strong positive capacity/performance evidence.12. Research philosophyPreserve the project-wide method:smallest falsifiable claim -> cheapest decisive test -> minimal verification -> expand only if warranted.Per substantive turn:one primary hypothesis;one minimum decisive test;provenance to exact paper/source/section/code;explicit PASS / FAIL / UNCLEAR / HUMAN_REVIEW;separate mechanism correctness from engineering failures;do not overclaim from incomplete native evidence;kill/park weak candidates quickly;reprioritize autonomously inside BOOT if one candidate dies.Human/PI remains responsible for final strategic/importance decisions; Research GPT performs search, derivation, comparison, falsification, source audit, minimal verification, and durable state maintenance.13. Continuous-autonomous policyCONTINUOUS_AUTONOMOUS_RESEARCH remains enabled across the session boundary.Rules:纯文本NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false

per-task Codex approval:
not required when it is the cheapest decisive authorized in-scope test

candidate substantive-turn soft budget:
8

candidate substantive-turn hard budget:
12At soft budget, review:information gain;mechanism progress;native signal;novelty potential;expected value of the next test.At hard budget, park by default absent:validated candidate;new meaningful claim;positive native signal;credible novelty;high-value next test.A failed candidate/family must be parked/killed and followed by autonomous in-scope reprioritization.Do not WAIT_PI merely because one candidate fails.WAIT_PI/`STOP` is legal only if the top-level BOOT research frontier is exhausted and must explicitly say:纯文本research_frontier_exhausted: true14. Codex delegation rulesWhen delegating:model must remain gpt-5.6-sol;reasoning must remain xhigh;ZERO_API_BILLING=YES;no paid API fallback;no silent model/effort downgrade;one task = one falsifiable objective;no unauthorized parameter sweep;no retries after a task's explicit no-retry boundary;preserve source/workdir/binary/evidence of pending/completed tasks;Codex evidence is never scientific PASS/FAIL until independently audited by Research GPT;pending tasks may cross Research GPT session boundaries;a pending task does NOT reserve a session-local research turn;when its result arrives, it PREEMPTS the next free substantive turn in the latest active session.15. Pending/background Codex/native provenanceThese are durable background records, NOT execution requests.They must not be restarted or duplicated.Task A纯文本task_id:
BOOT-B175-CASE1-L18-SI-POINTWISE-20261028-R3-01

origin_session:
密码学 10.0

origin_turn:
3

original_hypothesis:
BOOT-B175 CASE_1 single L18 SI pointwise falsification gate; exact full hypothesis remains in orchestrator.db because transport truncates it.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
51417

start_time:
2026-10-28T14:22:20.409Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
trueReported result excerpt: SOURCE_BLOCKED / PREREQUISITE_FAILED because the parent ZIP was not found at that moment. This was later superseded operationally by the retry task below. Do not rerun.Task B纯文本task_id:
BOOT-B175-CASE1-L18-SI-POINTWISE-20261028-R4-RETRY-01

origin_session:
密码学 10.0

origin_turn:
4

original_hypothesis:
Retry of the same authorized B175 CASE_1 single L18 SI pointwise falsification gate after acquisition-timing failure; full hypothesis remains in orchestrator.db.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
52565

start_time:
2026-10-28T14:35:12.005Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
trueReported result: decisive B175 pointwise FAIL with POINTWISE_REQUIRED_BITS=664, budget -15, mismatches 32767/32768. This evidence was already substantively incorporated into the durable BOOT scientific state; do not duplicate execution.Task C纯文本task_id:
BOOT-RMFE-R8-BSGS-MIDDLE-FIXEDQ-NATIVE-20261029-R14-01

origin_session:
密码学 11.0

origin_turn:
14

original_hypothesis:
Execute one source-faithful fixed-Q p=5,r=4 RMFE middle trace using exact six-KS R8 BSGS maps; full hypothesis remains in orchestrator.db.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
94049

start_time:
2026-10-29T02:11:15.820Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
trueReported result: SOURCE_BLOCKED / UNCLEAR; no native scientific execution. Artifact SHA-256:469a07c41f1a89bd838e4bf7ef57ab105673ca66561344955d8f9ab228fef0fc.Task D纯文本task_id:
BOOT-RMFE-P5W512-DETERMINISTIC-INSTANCE-MASK-GENERATOR-20261029-R16-01

origin_session:
密码学 11.0

origin_turn:
16

original_hypothesis:
Construct one deterministic paper-conforming p=5,w=512 RMFE instance, five exact projection constants, and restricted rank-5 R8 adapter; full hypothesis remains in orchestrator.db.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
95979

start_time:
2026-10-29T02:39:22.766Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
trueReported result: PASS deterministic plaintext instance and restricted rank-5 adapter. Artifact hash lineage is already incorporated into later static work. Do not rerun.Task E纯文本task_id:
BOOT-RMFE-P5W512-R8-CONSECUTIVE-BASIS-COMPOSED-GATE-20261029-R19-RECOVERY-01

origin_session:
密码学 11.0

origin_turn:
19

original_hypothesis:
Recovery/execution of the corrected consecutive-basis R8 composed plaintext gate J(phi(e_i))=Y^i, i=0..4; full hypothesis remains in orchestrator.db.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
13899

start_time:
2026-10-29T04:02:19.602Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
trueReported exact result: PASS / EXACT_IDENTITY_BOTH_PHYSICAL_SLOTS; retained matrix I_10, rank 10, no leakage/sign/scale/permutation discrepancy.Artifact:BOOT-RMFE-P5W512-R8-CONSECUTIVE-BASIS-COMPOSED-GATE-20261029-R18-01.zipSHA-256:519240d0de9c8a995a781da8071f242b18dd4ccd8be20f0474d46d78639eabe8Do not rerun.Task F — CURRENT HIGH-PRIORITY BACKGROUND RESULT纯文本task_id:
BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-NATIVE-20261029-R23-01

origin_session:
密码学 12.0

origin_turn:
23

original_hypothesis:
One-shot source-faithful p=5,r=1 RMFE one-core native canary in pinned HElib, with stage-by-stage static/native oracles, safe JSON recrypt instrumentation, scalar extractDigitsThin correctness oracle, capacity checkpoints, and conditional same-machine timing baseline; full original hypothesis remains in orchestrator.db.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
xhigh

pid_or_remote_execution_identity:
2578

start_time:
2026-10-29T14:18:23.408Z

current_status:
COMPLETED

expected_artifacts:
[]

evidence_status:
AVAILABLE

audit_status:
READY

result_delivered:
false

do_not_rerun:
trueReported Codex result excerpt:纯文本SOURCE_BLOCKED

fresh static preflight stopped at grouped-S2C canonical hash check
exit code 2

all R14/R16/R17/R18 ZIP outer/internal hashes:
PASS

R18 exact two-slot identity reverification:
PASS

tau_i(phi(e_j)) mod625:
25/25 PASS

tau_i(phi(e_j)) mod5:
25/25 PASS

no HElib build/context/key/encryption/native candidate stage/raw invariant/DigitExtract/timing executed

requested automorphisms:
0

actual KS applications:
0Artifact:纯文本/Users/bingwu/Developer/research-orchestrator/
BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-NATIVE-20261029-R23-01.zip

bytes:
103976

SHA-256:
c9c563be6a9e3e2a646822e55813d5e5048c229ed57116988bd40595dd7592f0Internal SHA256SUMS reportedly cover 37 files and ZIP integrity reportedly passes.Git reportedly remained:bb9e5d3413e75362c0f26f29bd3ec4d9bf64e11cThis task is background evidence only.DO NOT restart it.DO NOT duplicate it.DO NOT modify its source/workdir/binary.The successor must independently audit it before accepting SOURCE_BLOCKED scientifically.16. Cross-session pending-result rulePending/completed-but-unaudited Codex/native tasks are independent of Research GPT session boundaries.They remain background work.Never restart or duplicate them merely because a new conversation started.When a result is ready and not yet independently audited:it preempts the next free substantive research turn;restore the authoritative Git state first;audit artifact/provenance/source boundary independently;distinguish scientific PASS/FAIL from SOURCE_BLOCKED/UNCLEAR/instrumentation;only after audit update the scientific state;do not automatically launch a follow-up experiment unless it is the new cheapest decisive test and no other heavy task is occupying the local slot.17. Normal next iterationBecause the R23 result is already reported as AVAILABLE / READY but not independently audited, the successor's next free substantive turn should be:纯文本INDEPENDENT_AUDIT_R23_SOURCE_R1_PREFLIGHT_BLOCKPrimary question:Is the grouped-S2C canonical hash failure a legitimate source prerequisite mismatch, or an over-constrained hash check caused by deriving the correct mod-5 source-r=1 S2C from the mod-625 R14 map rather than expecting byte/hash identity with the old artifact?Do not rerun R23 while auditing.If audit confirms a purely preflight/hash instrumentation blockage and the scientific candidate was never executed, classify the native mechanism as UNCLEAR, not FAIL, and then choose the next cheapest decisive source-r=1 test under the continuous-autonomous policy.18. Strict ORCHESTRATOR_CONTROL protocol for every normal successor answerEvery normal substantive/control answer in 密码学 13.0 must end with exactly ONE control block and NOTHING after it.Continue research纯文本<ORCHESTRATOR_CONTROL>
action: CONTINUE
milestone: false
requires_pi: false
independent_research_available: true
</ORCHESTRATOR_CONTROL>Set milestone: true only when a real durable checkpoint/milestone was reached.Execute Codex/native taskUse only when execution is genuinely the cheapest decisive test and the local slot is free:纯文本<ORCHESTRATOR_CONTROL>
action: EXECUTE
task_id: UNIQUE_TASK_ID
milestone: false
requires_pi: false
independent_research_available: true
</ORCHESTRATOR_CONTROL>A complete <CODEX_TASK> block must appear immediately before the control block.Never execute a duplicate/pending/completed do_not_rerun task.Pending PI but independent work exists纯文本<ORCHESTRATOR_CONTROL>
action: CONTINUE
milestone: false
requires_pi: true
independent_research_available: true
</ORCHESTRATOR_CONTROL>A pending PI decision is advisory/nonblocking unless it actually blocks all useful independent work.WAIT_PIOnly when no useful independent work remains and the relevant PI decision genuinely blocks progress:纯文本<ORCHESTRATOR_CONTROL>
action: WAIT_PI
milestone: false
requires_pi: true
independent_research_available: false
research_frontier_exhausted: true
</ORCHESTRATOR_CONTROL>STOPOnly if the entire authorized top-level BOOT frontier is exhausted or an unrecoverable required-runtime blocker applies:纯文本<ORCHESTRATOR_CONTROL>
action: STOP
milestone: true
requires_pi: false
independent_research_available: false
research_frontier_exhausted: true
</ORCHESTRATOR_CONTROL>WAIT_PI or STOP without research_frontier_exhausted: true is invalid.When requires_pi: true, independent_research_available MUST always be present.Do not put trailing text after the control block.19. Successor behavioral boundaryAt session start:read GitHub authority at or after 62ba99ff9529bfd54f741796d8b4dbb8b9b57bc5;verify whether any newer commit changed BOOT state;restore TRACK_ID=BOOT, ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS;audit R23 first because its result is ready and unaudited;do not assume its SOURCE_BLOCKED classification is correct until independently verified;do not restart or duplicate any background task listed above;preserve all killed-claim boundaries;continue autonomous BOOT research only after the R23 audit determines the correct next cheapest decisive step.
