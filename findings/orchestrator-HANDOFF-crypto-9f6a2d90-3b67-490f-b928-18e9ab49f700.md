# 密码学 20.0 handoff

Resume research — Session Handoff

这是同一个持续进行的 FHE Bootstrapping 研究项目，不是新研究主题。

0. Session identity

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED: Research Turn 25/25 — Session milestone consistency checkpoint
LATEST_VERDICT: PASS_SESSION_MILESTONE_CONSISTENCY_CHECKPOINT
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE
PREVIOUS_SESSION_RESEARCH_TURNS: 25/25 COMPLETE
NEXT_ITERATION: Resume from this handoff, first reconcile the already-delivered native evidence below with durable state, then choose exactly ONE next cheapest decisive substantive test.
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
CONTINUOUS_AUTONOMOUS_RESEARCH: enabled
PENDING_PI_DECISIONS: none
RESEARCH_FRONTIER_EXHAUSTED: false

The completed read-before-write durable Git checkpoint is:

BBBINGW/memory main@fbe2a3ba42ee718e2eca0693836357c8d8b7fef4

Treat that commit as the authoritative post-session checkpoint. Do not overwrite it from memory or from stale earlier BOOT findings.

1. Roles and research protocol

Human PI has final authority over:

top-level research direction;
whether a gap/contribution is important;
acceptable assumptions/tradeoffs;
major pivots;
publication judgment.

Assistant acts as autonomous FHE research student and may:

search literature;
audit source;
derive mathematics;
falsify candidates;
design minimal tests;
park/kill/reprioritize candidates inside BOOT;
authorize cheapest-decisive Codex/native work when the local slot is free.

Default research philosophy:

smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted.

Each substantive Research Turn has:

ONE primary hypothesis;
ONE minimal decisive test;
explicit falsifier;
PASS / FAIL / UNCLEAR;
candidate disposition;
clear distinction between source fact, derivation, assumption, static model and native measurement.

Failed candidate/family:

KILL or PARK it;
autonomously reprioritize within BOOT;
do not WAIT_PI merely because one candidate failed.

PENDING_PI_DECISION is advisory and nonblocking:

pending PI decision + independent work available => continue reversible/no-regret work;
pending PI decision + no independent work => WAIT_PI;
inheritance alone never justifies WAIT_PI.

WAIT_PI or STOP is allowed only when the top-level research frontier is genuinely exhausted and must declare:
research_frontier_exhausted: true.

Candidate substantive-turn budget:

soft limit 8;
hard limit 12.

Do not silently treat implementation failure as mathematical impossibility or vice versa.

2. Canonical final scientific state from the completed session
2.1 Old aggregate-only candidate remains KILLED

The old architecture was:

five reconstructed dirty branch states
→ sum_i Y^i C_i
→ aggregate-only RM10 / joint recovery.

Final kill reason:

HElib deliberately permits full extension-valued dirty states before inverse thin projection. For arbitrary branch states,

F(C_0,...,C_4)=sum_i Y^i C_i

loses branch identity. Turn 13 established a kernel witness showing aggregate-only recovery cannot reproduce the stock branchwise scalar outputs on the full dirty domain. Turn 14 then removed the only remaining rescue by source-auditing HElib: inverse ThinEvalMap is explicitly designed to extract scalar semantics from dirty extension-valued slots, and key switching injects full-ring RLWE error.

Therefore:

old post-reconstruction aggregate-only delayed fusion = KILLED;
it is NOT reopened by the new candidate;
do not return to RM10/joint-map complement patching unless a genuinely new representation preserves branch information before loss.
2.2 Surviving candidate — canonical final pipeline

Fixed concrete instance:

p = 5
m = 32768
w = 512
k = 5
ell = 2
e = 4
e' = 1
temporary plaintext space = 625
local extension degree d = 8192.

Canonical coordinate set:

J = {0,1024,7168,2048,6144}
= {0,+1024,-1024,+2048,-2048} mod 8192.

Canonical FOUR-output joint branch labelling in J order:

[2,0,3,1,4]

This supersedes:

Turn 15 initial J={0,1024,2048,3072,4096};
Turn 18 L0-only optimal labelling.

Canonical path:

Aung SlotsToCtxts
→ five scalar thin ciphertexts
→ sparse power-coordinate packing on J
→ one rho-compensated shared forward transform
→ one source-identical HElib recryption middle
→ pure power-basis inverse, normal_basis=false semantics
→ 17-call target-pruned binary unpack
→ five scalar Z_625 lifts
→ four RMFE correction recombinations L0,L1,L2,L3
→ Aung Algorithm 4 correction DigitExtract
→ restore original intFactor at the stock final point.

Important:
Turn 21 shorthand “recombine z → Algorithm 4” is superseded. A correct implementation MUST generate L0,L1,L2,L3 first.

Candidate inverse MUST use pure power-basis / normal_basis=false semantics. Never use stock firstMap(normal_basis=true) and then interpret its coordinates as power-basis leaves.

3. Static correctness theorem

Status:

STATICALLY CLOSED, CONDITIONAL ON THE STANDARD HELIB RECRYPTION CORRECTNESS/NOISE BOUND.

The required theorem is standalone plaintext correctness, NOT transcript equality to the five stock MultKey branches.

The shared middle only needs ordinary HElib recryption correctness:
after reconstruction the temporary plaintext is a p-adic lift of the packed source plaintext.

Because the pure inverse is Z_625-linear, selected power-basis coordinates retain the correct source residues modulo 5 even when arbitrary higher 5-adic dirty terms exist.

Pruned unpack then returns five actual base-ring scalars:

a_i in Z_625.

Only after scalar recovery form:

L_t(z) = sum_i a_i * phi(e_i)^(5^t), t=0,1,2,3.

Thus each correction ciphertext is exactly in the intended RMFE image/type. Higher 5-adic digits may remain dirty.

Current eta:

eta = 125 = 5^3 = p^(e-1),

matching the correction Algorithm-4 requirement established in the session.

Not established:

native ciphertext correctness of the new candidate;
empirical DFR;
final bitCapacity;
native latency/throughput.
4. rho / basis details

Turn 16 corrected the false intermediate statement that forward ThinEvalMap equals full EvalMap on arbitrary extension values.

For the current one-factor temporary algebra, full forward Step1 factorizes as:

FullForward(a,b) = A * (a, rho(b))

where

A = [[1,1],[443,182]]

and the pure inverse is

A^-1 = [[313,91],[313,534]] mod 625.

rho maps the selected nonzero coordinates within J, with public unit 182.

rho^-1 unit correction:

182^-1 = 443 mod 625.

Unpack normalization:

8192^-1 = 28 mod 625.

The rho permutation/unit is folded into the public RMFE correction constants; no extra automorphism is required.

5. Pruned unpack and transform schedule

Target-pruned binary unpack:

physical Frobenius calls = 17.

Distinct Frobenius exponents:

4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1.

Per-selected-leaf Frobenius depth = 13.

Active-node counts:

[1,1,1,1,1,1,1,1,1,1,1,2,4]

Retained add/sub count = 21.

Monomial plaintext multiplications = 5, all canonical norm 1.

Recovery-side physical KS:

candidate:
1 pure-inverse outer automorphism

17 shared Frobenius
= 18.

Stock five-branch inverse recovery:

5 * (1 outer + 13 trace Frobenius)
= 70.

Per-output KS depth:
candidate = 14;
stock = 14.

Including the one shared forward transform:

candidate transform-side count = 19
stock transform-side count = 75.

CRITICAL CLAIM BOUNDARY:

“19” means ONLY transform-side automorphism/KS schedule.

Do NOT describe it as:

“19 total operations”;
“MultKey costs only 19 operations”;
a latency prediction.

The candidate still pays:

sparse packing;
one full shared HElib recryption middle;
21 unpack additions/subtractions;
four five-way RMFE correction recombinations;
full Algorithm-4 DigitExtract.

Only the preregistered end-to-end native gate decides systems value.

6. Static public-cost ledger

Turn 17:

normalized pure-inverse + 13 split levels conservative fixed-Q public factor:

62 * 8192 = 507904

log2 = 18.954196310386877 bits.

This EXCLUDES automorphism/key-switch noise.

It is a local deterministic triangle ledger, NOT an additive prediction of final HElib bitCapacity.

One-time sparse packing:

factor = 5
tax = log2(5) = 2.321928094887362 bits.

Turn 22 four-output correction audit, canonical labelling [2,0,3,1,4]:

L0 candidate-vs-stock delta = -0.213245426290 bits
L1 delta = -0.332235477742 bits
L2 delta = -0.157598507289 bits
L3 delta = -0.405765059070 bits.

Thus all four correction recombinations are no worse than stock under the same public-multiplier norm ledger.

7. Key-switch/noise structure

Under HElib FULL Frobenius setup:

addFrbMatrices generates direct key-switch matrices for every nonidentity Frobenius power.

Therefore the 17 requested candidate Frobenius calls are one-hop direct KS calls, not hidden multi-hop smartAutomorph chains.

For a selected unpack leaf, the tracked structural recurrence is:

B_(t+1) <= 2 B_t + K_t.

Under uniform K:

B_13 <= 8192 B_0 + 8191 K.

This is the same binary-trace recurrence/depth as stock HElib traceMap at d=8192.

Sibling-only KS noise does not flow back into a selected leaf.

If a future benchmark uses BSGS/MIN Frobenius resources rather than FULL, physical call count and key-memory comparison MUST be recomputed. Never silently compare a FULL-key candidate to a reduced-key baseline.

8. Implementation contract

No evaluator secret key is required.

No new cryptographic primitive is required.

No new security assumption is introduced.

Under FULL setup, no new evaluation-key TYPE is needed.

Current HElib public API alone is insufficient for a clean source-faithful external implementation because:

PubKey::recryptKeyID is private;
PubKey::recryptEkey is private;
newMakeDivisible is file-static in src/recryption.cpp.

This is an encapsulation blocker, not a cryptographic blocker.

Minimal safe HElib patch:

factor the source-identical preprocessing body into one narrow internal/source-shared PubKey member/helper, conceptually:

preprocessForRecryption(Ctxt& ctxt)

performing the existing stock sequence:

drop/mod-down
→ reLinearize(recryptKeyID)
→ rawModSwitch(q)
→ stock noise check
→ newMakeDivisible
→ divide by p^e'
→ ctxt = recryptEkey
→ multByConstant(zzParts[1])
→ addConstant(zzParts[0]).

Stock reCrypt/thinReCrypt and the candidate should use the SAME helper.

Do NOT expose recryptEkey or recryptKeyID publicly.

9. Novelty boundary — final state

Broad novelty claims KILLED:

Geelen binary unpack recurrence is new;
only recovering useful coefficients is new;
“Partial CoeffToSlot” is new;
packing multiple ciphertexts before a shared bootstrap is new;
one shared bootstrap middle is new;
unpack before digit extraction/removal is new;
high-level direct RMFE MultKey objective is new.

Direct high-level collision:

Geelen–Vercauteren ePrint 2024/1587 §5.5,
“Batch Bootstrapping via Packing”.

That work already establishes:

pack multiple ciphertexts
→ shared bootstrapping work
→ unpack before digit removal/extraction.

Therefore current publication claim MUST NOT be “batch bootstrap via packing”.

No exact collision was found in the completed audit for the narrower complete mechanism:

RMFE dirty-state aliasing obstruction;
information-loss proof for aggregate-only delayed fusion;
rho-stable sparse power-coordinate representation of the five RMFE branch identities;
pure power-basis inverse;
target-trie pruning of Geelen’s binary unpack to the five selected coordinates;
construction of all four Aung correction ciphertexts only after scalar recovery.

Search absence is NOT novelty proof.

Pruned tree alone is likely too obvious/weak for a strong-paper contribution.

Potential contribution, if native value is strong, is the full obstruction→repair story.

Publication novelty status:

NARROW / CONDITIONAL / NOT YET PROVEN.

10. Preregistered future native decision matrix

The future native test for the NEW partial-unpack candidate is preregistered.

Primary comparator:

same-build source-faithful Aung Corr./TnM
with IDENTICAL FULL Frobenius key resources.

Resource parity:

same HElib commit;
same compiler/flags;
same thread count;
same Context/key object;
same FULL Frobenius resource;
key generation outside timed region for both;
RMFE constants / candidate tables outside timed region;
EvalMap cache construction outside timed region;
same encrypted input copied before each paired branch.

Correctness is a HARD FIRST GATE.

Required patterns:

all zero;
all one;
all four;
alternating zero/four;
five RMFE basis-unit patterns;
32 fixed seeded random cases.

For every case require:

candidate decrypt == source plaintext;
candidate decrypt == stock Corr./TnM decrypt;
all Algorithm-4 divideByP operations satisfy debug/source-faithful divisibility;
final ptxtSpace/intFactor semantics match stock;
exactly five pruned leaves in audited order;
correction tuple exactly L0,L1,L2,L3.

Any one failure:

FAIL_CORRECTNESS.

Do not interpret timing after a correctness failure.

Timing:

3 warmups;
20 measured paired runs;
alternating AB/BA;
primary metric = median paired candidate/baseline latency ratio;
report mean, p90 and paired-ratio 95% bootstrap CI.

Capacity/depth:

final bitCapacity;
minimum bitCapacity among L0..L3 before DigitExtract;
same post-bootstrap remaining-multiplication test as Aung/stock.

Pre-registered labels:

STRONG_PASS:

correctness passes;
paired median latency ratio <= 0.80;
95% CI upper <= 0.90;
remaining multiplications >= 5;
throughput >= matched thin;
no hidden key-resource increase.

VALUE_PASS:

correctness passes;
paired median latency ratio <= 0.90;
95% CI upper <= 1.00;
remaining multiplications >= 5;
throughput improves >=10% over matched Corr./TnM.

PARETO_PASS:

latency gain <10%;
but strict declared improvement in capacity/depth/key-memory/RSS under resource parity.

PARK:

correctness passes;
no >=10% latency gain;
no strict secondary-frontier improvement.

FAIL_VALUE:

slower than matched baseline;
no capacity/depth/memory compensation.

KILL_CAPACITY:

final bitCapacity < 70;
or catastrophic source-equivalent remaining-depth failure.

Do not modify these labels after observing native results.

11. Published external sanity reference

Aung p=5 Corr./TnM Table-2 stage timings:

SlotsToCtxts = 2.284 s
MultKey = 4.732 s
CtxtsToSlots = 0.078 s
DigitExtract = 4.240 s

sum = 11.334 s.

Published p=5 Corr./TnM:

final capacity ≈101;
remaining multiplications = 5;
latency ≈11.3 s;
throughput = 89.08.

Published thin:

capacity = 151;
remaining multiplications = 8;
latency = 2.82 s;
throughput = 107.06.

These are external sanity references only. Primary systems verdict must be same-machine paired.

12. Latest Codex/native evidence — already completed and delivered

There is one durable Codex task provenance record.

It is COMPLETED, evidence is AVAILABLE, result has already been DELIVERED, and it MUST NOT be restarted or duplicated.

This task tested the OLDER current/post-raw candidate path, not the new Turn-15--25 sparse-pack/pruned-unpack candidate.

Its result stopped at the baseline comparator and therefore does NOT give a native verdict on the new candidate.

Exact provenance:

task_id:
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

origin_session_id:
1f28610c-0aa3-4cce-9ec9-158d114c5ae8

origin_session:
密码学 17.0

origin_turn:
4

original_hypothesis:
TASK_ID: BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
Research Turn 4/25 — paired same-machine throughput gate

结果：`PASS_PAIRED_SAME_MACHINE_NATIVE_GATE_CONTRACT`

这一轮发现并修正了一个重要实验口径问题：下一步不能只在本地测 candidate recovery latency，再把这个秒数代入 Aung 论文的 2.909962 s middle-budget。 Aung 的绝对时间来自 Xeon 8368Q，而 R4/native result 来自另一执行环境；混用两套硬件的秒数不能形成严格 throughput verdict。

因此下一次实验改成同机 paired comparison，三条路径全部使用：

同一 HElib commit acdb264…
同一 m=32768,p=5,r=1,bits=400
单线程
同一 BSGS+10 direct-RM10 keyset
同一 warmup / measurement protocol

比较对象固定为：

vanilla HElib thin；
source-faithful Aung Corr./TnM；
当前 post-raw fusion candidate。

这里特意让 baseline 和 thin 也使用 BSGS+10，因此 candidate 没有 keyset 优势；实际上额外 direct matrix 还会帮助 baseline，比较是偏保守的。注意 HElib 的 BSGS key-switch strategy 与 Aung 的 Corr./BSGS workflow 是两个不同概念，prior comparator 仍然是 Corr./TnM。

同机主指标改为：

R_prior = C_cand T_prior / (C_prior T_cand)

以及

R_thin = 5 C_cand T_thin / (C_thin T_cand)

其中 factor 5 来自 candidate 有 10 packed slots，而 thin 有 2 slots。

判据已经固定：

STRONG_PASS:
lower95(R_prior) > 1
AND lower95(R_thin) > 1

NO_PRIOR_WORK_GAIN:
upper95(R_prior) <= 1
=> KILL current candidate on systems value

PRIOR_ONLY_PASS_BUT_THIN_FAIL:
lower95(R_prior) > 1
AND upper95(R_thin) <= 1
=> PARK / low publication value absent distinct novelty

UNCLEAR:
CI straddles 1

任何 candidate correctness mismatch 都先返回 FAIL_NATIVE_CORRECTNESS，不允许继续解释 performance；如果 RM10 不是 10 个 direct physical KS、joint recovery 不是 4 个 chained j=1 KS，则返回 FAIL_EXECUTION_CONTRACT，说明测错了实现而不是 scientific failure。

下一次 native gate 还必须直接跑到 correction DigitExtract / final recode，记录 final capacity，因此一次实验同时关闭：

latency；
final capacity；
final correctness；
thin-throughput comparison；
physical-hop audit；
absolute key bytes。

正式任务已经建立：

BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

范围固定为 5 warmups + 20 measured runs / workflow，无 sweep、无 rescue、无 alternative candidate。

详细 contract 已持久化并读回验证：

findings/boot-RMFE-paired-same-machine-throughput-native-gate-contract-2026-11-01.md

当时 durable authority：

BBBINGW/memory main@a55349a44cb83471e2c8e82a57fef5c52fb5e128

这一步之后，继续做静态 latency operation-count 推断的信息增量已经明显低于执行这个 paired native gate。

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

durable_evidence_reference:
orchestrator.db codex_tasks.task_id=BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

result_excerpt:
FAIL_NATIVE_CORRECTNESS

Vanilla thin correctness passed.
Source-faithful Aung Corr./TnM failed correctness on the first smoke run.
Contract required immediate stop.
Candidate was NOT executed.
No performance, capacity, CI or throughput verdict was produced or may be inferred.
RM10/joint physical-hop audit was never reached.
Exact 741 MiB keyset was persisted and may be reused; do not regenerate it unnecessarily.
This result is therefore a comparator-implementation/native-harness blocker, not evidence that the new Turn-15--25 candidate is scientifically false.

Key evidence paths:

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-run.log
/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-progress.jsonl
/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/source/benchmark.cpp

Cross-session lifecycle rules:

This task is inert completed provenance.
Do NOT rerun, duplicate, modify its source/work directory/binary, or regenerate its long-lived keyset merely to reproduce it.
Before starting any future native candidate gate, first determine whether the Corr./TnM comparator mismatch has already received an independent durable audit.
If no durable audit exists, the next relevant native-side research step is to audit the comparator mismatch using the existing evidence/artifacts rather than submitting another heavy job.
If it has already been independently audited and repaired in durable state, proceed from that audited state.
Never interpret this completed task as a performance failure of the new sparse-pack/pruned-unpack candidate because that candidate was never run.
13. Session accomplishments / major verdicts

Turns 14–25 final arc:

Turn 14:
FAIL_HIDDEN_PREFUSION_THIN_STATE_INVARIANT.
Source showed stock thin path explicitly accepts dirty extension state; old delayed aggregate architecture killed.

Turn 15:
PASS_PRUNED_DIRTY_SLOT_PARTIAL_UNPACK_REPAIR_GATE.
New identity-preserving pre-middle sparse-coordinate candidate found.

Turn 16:
PASS_FULL_EVALMAP_COORDINATE_TRANSPORT_REPAIR.
Corrected thin/full basis mismatch using rho-stable J.

Turn 17:
PASS_PRUNED_UNPACK_NO_STATIC_PUBLIC_CAPACITY_KILL.
17-node unpack deterministic public ledger did not statically kill candidate.

Turn 18:
PASS_REMAINING_PUBLIC_CONSTANT_LEDGER.
Sparse packing/rho/RMFE public constants did not statically kill candidate.

Turn 19:
PASS_PRUNED_TREE_KS_DEPTH_AND_NOISE_STRUCTURE.
Per-output KS depth stayed 14, equal to stock; 17 physical shared Frobenius calls under FULL keys.

Turn 20:
PASS_TARGETED_PRIOR_ART_NO_EXACT_COLLISION.
No exact target-pruned mechanism collision found, but broad partial-extraction novelty killed.

Turn 21:
PASS_NEW_PARTIAL_UNPACK_STATIC_PADIC_INTERFACE.
New candidate obtained static p-adic semantic closure; later four-output implementation correction applied.

Turn 22:
PASS_IMPLEMENTATION_CONTRACT_WITH_ONE_INTERNAL_HELIB_HOOK.
Completed L0,L1,L2,L3 contract; final joint labelling [2,0,3,1,4]; one internal HElib hook sufficient.

Turn 23:
PASS_FUTURE_NATIVE_PREREGISTRATION_READY.
Future native decision matrix frozen.

Turn 24:
FAIL_BROAD_PREMIDDLE_PACK_SHARED_BOOTSTRAP_NOVELTY.
Geelen–Vercauteren 2024/1587 directly prior-discloses batch packing/shared bootstrap/unpack-before-digit-removal.

Turn 25:
PASS_SESSION_MILESTONE_CONSISTENCY_CHECKPOINT.
Cross-turn state consistent after explicit supersession rules.

14. Important killed/parked routes

Keep killed unless a genuinely new assumption/representation changes the falsifier:

naive additive preprocessing without carry;
universal “raw rounding forces all fusion post-raw” claim;
current post-reconstruction aggregate-only delayed fusion;
hidden pre-fusion rank-5/thin dirty-state invariant;
RM10-alone active-domain closure;
existing 5-term joint map complement annihilation;
p-divisible complement as sufficient DigitExtract-safe condition;
aggregate-only full-domain recovery;
8-term full-R8 zero-extension as a repair for branch-identity loss;
high-level direct RMFE MultKey novelty;
joint rank-5 recovery standalone novelty;
broad batch-packing/shared-bootstrap novelty;
“partial CoeffToSlot” novelty;
“only recover useful coefficients” novelty;
Geelen binary unpack recurrence novelty;
cross-branch stock HElib hoisting;
representation-only RMFE s=2 rescues;
high-level single-linear-phase novelty;
B175 direct SI pointwise route.

Old aggregate-only 19-call candidate is permanently distinct from the new partial-unpack 19-call transform schedule.

15. Strongest current candidate / main hypothesis

Strongest candidate:

RMFE branch identities can be preserved through one shared HElib recryption middle by sparsely encoding the five scalar branches into a rho-stable set of power-basis coordinates, then recovering only those coordinates using a target-pruned Geelen binary unpack tree, and only afterward constructing Aung’s four RMFE correction ciphertexts.

Current scientific status:

static correctness: PASS conditional on standard HElib recryption bound;
implementation feasibility: PASS with one internal HElib hook;
static public-cost blockers: none found;
KS-depth blocker: none under FULL resource;
native correctness/value: UNKNOWN;
exact novelty: NARROW / CONDITIONAL.
16. Recommended next cheapest decisive test

Do not start anything in the handoff itself.

On the successor’s first free substantive Research Turn:

Read the durable checkpoint at main@fbe2a3ba42ee718e2eca0693836357c8d8b7fef4.
Verify whether the already-delivered FAIL_NATIVE_CORRECTNESS comparator mismatch from task
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
has already received a separate durable independent audit.
If not, the highest-EIG cheapest decisive step is a bounded comparator-implementation audit using the existing log/progress/source and persisted keyset:
determine whether the source-faithful Aung Corr./TnM smoke mismatch is an implementation/harness error, basis/intFactor/Algorithm-4 ordering error, or a genuine source-comparator issue.
Do NOT rerun the heavy 5.5-hour key generation.
Do NOT run the new candidate until the comparator is trustworthy.
If that comparator result has already been durably audited elsewhere, choose the next cheapest decisive test from the new candidate’s preregistered gate rather than reopening static bookkeeping.
Only one primary hypothesis per turn.

This recommendation is provisional workflow guidance, not a new result.

17. Durable Git / artifacts / SHA256

Durable repository checkpoint:

BBBINGW/memory main@fbe2a3ba42ee718e2eca0693836357c8d8b7fef4

Key session artifacts created before the durable checkpoint:

Turn 25:

BOOT-T25-SESSION-MILESTONE-CONSISTENCY-CHECKPOINT-20261101.md
SHA256: 6d5256b6f9f08576681a76d8df1fcddd38ef652fe40c8818cf976aa7537ed15d
BOOT-T25-SESSION-CHECKPOINT-20261101.json
SHA256: 943d8d912359cbe3a0217577cdccff514452341bc2528f34562e64357d3d4c54

Turn 24:

BOOT-T24-CITATION-FORWARD-NOVELTY-BOUNDARY-GATE-20261101.md
SHA256: 97ac50afc012073c9464187979f6f620bdb1c3722e49c74268c6b5b9fc35bf6d

Turn 23:

BOOT-T23-FUTURE-NATIVE-PREREGISTRATION-GATE-20261101.md
SHA256: f90662b613c1205b3c18f8efa62d363cac46f9fcded80685ca0b646560de7bdd
BOOT-T23-FUTURE-NATIVE-DECISION-MATRIX-20261101.json
SHA256: 0475c581f9388811965a35bf0f7fbc0439f0d5be24060e7454d89c362c7ba4a8

Turn 22:

BOOT-T22-IMPLEMENTATION-CONTRACT-FOUR-CORRECTION-GATE-20261101.md
SHA256: 89c632bdf2cd791b1c3ada6dca592fdf3333a6be29d7ae1e1f7b1c92c2d11236
BOOT-T22-FOUR-CORRECTION-RECOMBINATION-CHECK-20261101.py
SHA256: 06238de2cf519e9790b9dcaf6a17f836fec68eb8961ed2ff8102677f9def52ee
BOOT-T22-FOUR-CORRECTION-RECOMBINATION-VALUES-20261101.txt
SHA256: 4a06957822d343a54d1803ff821d89f1252ea9ed5de34bf01b04ff00a5621cd1

Turn 21:

BOOT-T21-NEW-PARTIAL-UNPACK-STATIC-PADIC-INTERFACE-GATE-20261101.md
SHA256: 226d9f0fa5f600a6cdf9e97254ae6fab7722df3207f79473503aadc8ad9ee550
BOOT-T21-PADIC-INTERFACE-CONTROL-20261101.py
SHA256: 2a379764724581f862a54562c7e27820c0168146fcf0466f7ae1f45f1bbeb23a

The Turn-25 audit verified 21 Turn-14–24 artifacts present in its working environment.

18. Codex delegation rules

Codex/native work may cross Research GPT session boundaries.

Do not:

duplicate a completed or running task;
resubmit a task merely because a Research GPT session changed;
modify a running task’s source/workdir/binary;
claim a result before it is delivered;
reserve a session-local turn waiting for a task.

When a newly completed native result is delivered:

it preempts the next free substantive turn in the latest active session for independent audit;
audit result provenance and execution contract before scientific interpretation.

Cheapest-decisive Codex execution does not require per-task PI authorization while CONTINUOUS_AUTONOMOUS_RESEARCH is enabled, but:

only one heavy local/native slot at a time;
avoid expensive native work when a static/cheap falsifier exists;
correctness failures stop performance interpretation;
preserve exact task provenance.

The completed task listed above is do_not_rerun=true.

19. Strict successor control protocol

Every NORMAL substantive answer in the new conversation must end with exactly one control record.

Use this exact field set:

<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

Rules:

CONTINUE:
independent research remains and no new external execution is being launched in that answer.

EXECUTE:
use only when launching an actually established Codex/native task.
Include:
task_id: ...
inside the control record, but only when that exact identifier has been established.

WAIT_PI:
only if PI input is genuinely required AND no independent research remains.
Must additionally include:
research_frontier_exhausted: true

STOP:
only when the top-level research frontier is exhausted.
Must additionally include:
research_frontier_exhausted: true

independent_research_available must always be present; in particular it must be explicit whenever requires_pi: true.

Do not use WAIT_PI merely because a PENDING_PI_DECISION was inherited.

If action=EXECUTE, never silently launch a second heavy native task while another heavy task is active.

HANDOFF-only turns are an exception: when explicitly commanded to return machine handoff blocks, follow that handoff format instead of emitting a normal control block.

20. Successor opening discipline

Conversation name is fixed by the orchestrator:

密码学 20.0

At session start:

restore BBBINGW/memory main@fbe2a3ba42ee718e2eca0693836357c8d8b7fef4;
do not rely on stale STATE.md topic selection over this explicit BOOT handoff;
maintain TRACK_ID=BOOT;
maintain ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS;
recognize Research Turns 1–25 of 密码学 19.0 are complete;
start a fresh successor-session turn count only according to the orchestrator’s session protocol;
do not reinterpret the completed native task as a result for the new candidate;
first reconcile/audit existing delivered evidence when relevant;
then choose exactly one next cheapest decisive hypothesis/test.

No PI authorization is required for the next reversible, in-scope research iteration.
