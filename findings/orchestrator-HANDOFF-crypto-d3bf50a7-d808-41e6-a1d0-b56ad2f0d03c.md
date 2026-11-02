# 密码学 22.0 handoff

Resume research — Session Handoff

You are the successor research session to the completed ordinary-Chat BOOT session. This is the SAME logical FHE bootstrapping research program, not a new topic.

0. Runtime / role

Surface: ordinary Chat, not Work.
Research model: GPT-5.6 Sol.
Research style: act as an FHE research student under a human PI.

CONTINUOUS_AUTONOMOUS_RESEARCH remains enabled. Per-iteration PI authorization is not required for reversible, low-regret, cheapest-decisive research.

Primary philosophy:

纯文本
smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted

One research iteration = ONE primary hypothesis + ONE minimal decisive test.

Core principle:

纯文本
先证明有洞，再想怎么填；先 falsify，再 optimize。

Do not optimize a candidate already killed by a stronger obstruction. Failed families should be killed/parked and followed by autonomous in-scope reprioritization. WAIT_PI/STOP is allowed only if the whole top-level BOOT frontier is exhausted.

1. Durable authority

GitHub Notes is unhealthy.

The verified local BBBINGW/memory clone is the durable authority.

The read-before-write checkpoint for the completed session succeeded at:

纯文本
bc0fab910d1ca741741afc4d1cb3912204e2c047

Treat this commit as the authoritative session checkpoint.

Do not claim connector-derived Git facts unless independently verified in the successor environment.

The stale STATE.md excerpt mentioning CGS is not the active research direction. Explicit BOOT session authority and this handoff override it.

2. Current research identity
纯文本
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED: Research Turn 25/25 — BGV hidden-scaling / exact reconstruction-linearity gate
NEXT_ITERATION: successor-session Research Turn 1; restore this handoff first, then choose the next cheapest decisive BOOT test
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE

Research Turns 1–25 of the completed session are finished. Do not retroactively create another Turn 25.

No PI decisions are pending:

纯文本
PENDING_PI_DECISIONS: none

PENDING_PI_DECISION remains only an advisory queue. In future, inheritance of a PI decision never automatically implies WAIT_PI; separately determine whether independent research remains.

3. Canonical strongest candidate

The current strongest BOOT candidate is:

纯文本
PRE-TAG + POST-DIVIDE LATE AGGREGATION

Canonical pipeline:

纯文本
Aung SlotsToCtxts
→ five scalar thin branches C_i
→ branch-local global monomial tags G_i
→ five stock forward ThinEvalMap calls
→ five independent source-identical preprocessing paths:
     canonicalize / modDown
     → reLinearize(recryptKeyID)
     → rawModSwitch(q=626)
     → newMakeDivisible(5)
     → divide by 5
→ obtain five public post-divide pairs (z0_i,z1_i)
→ Z0 = Σ_i z0_i
   Z1 = Σ_i z1_i
→ ONE recryptEkey reconstruction:
     R = E·Z1 + Z0
→ ONE pure power-basis inverse
→ target-pruned full-domain binary unpack
     17 physical Frobenius calls
→ five scalar Z_625 lifts
→ four rho-correct RMFE correction outputs L0,L1,L2,L3
→ Aung Algorithm 4 / DigitExtract
→ restore original application intFactor at the stock final point

The aggregation boundary is precisely:

纯文本
AFTER branch-local rawModSwitch → newMakeDivisible → /5
BEFORE recryptEkey reconstruction

There is NO current pre-raw or pre-newMakeDivisible branch aggregation.

4. Frozen parameters and coordinates

Canonical parameters:

纯文本
p = 5
m = 32768
w = 512
k = 5
r = 1
e = 4
e' = 1
q = p^e + 1 = 626
temporary plaintext modulus = p^(e-e'+r) = 625
local extension degree d = 8192
RMFE eta = 125

Canonical selected coordinate set:

纯文本
J = [0,1024,7168,2048,6144]
  = {0,+1024,-1024,+2048,-2048} mod 8192

Canonical FINAL four-output branch labelling in J order:

纯文本
[2,0,3,1,4]

Do NOT use the stale single-output labelling [3,0,2,1,4].

Coordinate transport:

纯文本
rho(X^0)    = X^0
rho(X^1024) = 182 X^7168
rho(X^7168) = 182 X^1024
rho(X^2048) = 182 X^6144
rho(X^6144) = 182 X^2048

182^-1 = 443 mod 625
8192^-1 = 28 mod 625
5. Main static theorem chain
A. Early fusion obstruction remains real

Earlier session results remain valid:

exact ordinary branch mixing does not commute through rawModSwitch;
exact additive target maps into coprime q=626 are impossible in the required sense;
proper source-RNS subsets cannot retain enough Q-torsion;
post-KS public representative has full-ring support under the stock validity contract;
generic aggregate-only recovery from arbitrary post-reconstruction full-ring states is impossible;
newMakeDivisible / reconstruction disturbance spans the full ring, so no rank-5 dirty-state invariant is available.

Do NOT resurrect naïve pre-raw fusion.

B. Turn 13 make-divisible carry refinement

Once exact branchwise raw integer outputs are known, newMakeDivisible → /5 is not a fundamental information barrier.

For an integer mixing row a:

纯文本
A D(z) = D(Az) - q C_A(z)

with the commutator determined by mod-5 information.

This refined, but did not by itself rescue, early fusion.

C. Turns 14–17 raw commutator work

The rawModSwitch commutator can be compressed to a small carry.

For row [1,1]:

纯文本
C_raw ∈ {-1,0,1}

and more generally:

纯文本
C_raw(a;c) = round(Σ_i a_i f(c_i))

for centered CRT fractional phases f.

However:

exact universal low precision fails;
all active source primes are still required for universal exactness;
HPS-style fractional CRT / certified fallback is prior art;
this carry path became secondary after the late-aggregation placement was found.

Do NOT treat the HPS carry kernel as required machinery for the current primary candidate.

D. Turn 18 late aggregation

This is the key architectural repair.

Each tagged branch independently crosses every nonlinear preprocessing step. Only post-divide integer pairs are aggregated.

For a fixed recryptEkey ciphertext E:

纯文本
R_i = E*z1_i + z0_i

and:

纯文本
R_shared
  = E*(Σ z1_i) + Σ z0_i
  = Σ_i (E*z1_i + z0_i)
  = Σ_i R_i

The shared reconstructed plaintext has source-shaped form:

纯文本
F(Σ_i G_i m_i) + 5 E_dirty

and after the pure inverse:

纯文本
Σ_i G_i m_i + 5 E'_dirty

Therefore selected J coordinates retain the intended branch values modulo 5, while arbitrary higher 5-adic and nonselected dirty coordinates are tolerated by the full-domain pruned unpack.

No rank-5 dirty-state invariant is claimed or needed.

E. Turn 23 tagged ThinEvalMap typing theorem

Generic forward ThinEvalMap is NOT the full EvalMap on arbitrary extension-valued inputs.

But for one Aung branch with scalar physical slots (a,b), multiplication by global monomial X^j produces actual physical slots:

纯文本
(a X^j, b rho(X^j))

Stock forward ThinEvalMap applies the scalar two-slot matrix:

纯文本
A = [[1,1],[443,182]]

and because b is a base-ring scalar:

纯文本
rho(b X^j) = b rho(X^j)

hence exactly:

纯文本
ThinForward(Tag_j(a,b))
  = FullForward(a X^j, b X^j)

over Z_625.

So five branch-local tagged forwards are correctly typed.

Never restore the false broad claim that ThinEvalMap works generically on arbitrary extension-valued slots.

F. Turn 25 actual HElib BGV hidden scaling

Pinned HElib addConstant(ZZX) scales constants by:

纯文本
f_E = bal_625(intFactor_E * (Q_E mod 625) mod 625)

where Q_E is the product of recryptEkey's ciphertext primes.

Thus actual stock reconstruction is:

纯文本
R_E(z0,z1)
  = DCRT(z1) * E
    + f_E * DCRT(z0)

not literally unscaled E*z1+z0.

But multByConstant(ZZX) does NOT change:

ptxtSpace;
intFactor;
primeSet.

All hypothetical branch reconstructions begin from the SAME recryptEkey, so the same f_E applies to every branch.

Therefore:

纯文本
R_E(Σ z0_i, Σ z1_i)
  = Σ_i R_E(z0_i,z1_i)

EXACTLY at ciphertext-part level.

Ctxt::addCtxt also performs no BGV factor harmonization because every hypothetical branch reconstruction has the same intFactor, ptxtSpace=625, and prime set.

Verdicts:

纯文本
PASS_BGV_HIDDEN_SCALE_RECONSTRUCTION_LINEARITY
PASS_EXACT_CIPHERTEXT_PART_LATE_AGGREGATION_EQUIVALENCE
PASS_NO_BRANCH_INTFACTOR_HARMONIZATION
6. Noise/capacity state

Turn 19 established a conservative one-factor-five late aggregation envelope:

纯文本
B_shared <= Σ_i B_i <= 5 B_max

so:

纯文本
log2(5) = 2.321928094887 bits

is a valid deterministic worst-case sensitivity factor.

Turn 25 refined this:

all hypothetical branch reconstructions reuse the SAME fixed boot-key ciphertext E, so the boot-key noise realization is shared:

纯文本
Σ_i z1_i E
  = (Σ_i z1_i) Enc(s_R)
    + (Σ_i z1_i) η_E

not five independent η_E samples.

Therefore factor five is a safe WORST-CASE upper bound, not a mandatory paid penalty. Direct fused HElib noise tracking may be materially tighter.

Final four-output recombination worst candidate-vs-stock delta:

纯文本
-0.157598507289 bits

Canonical late-sum + recombination sensitivity envelope:

纯文本
2.321928094887 - 0.157598507289
= 2.164329587598 bits

Do NOT use stale 2.016729 bits.

Local normalized inverse + 13 split-addition public ledger:

纯文本
18.954196310387 bits

Deliberately pessimistic INVALID-AS-PREDICTION stress:

纯文本
C_stress
= 101
  - 18.954196310387
  - 2.164329587598
= 79.881474102015 bits

Static hard-kill line:

纯文本
69.845944 bits

Margin:

纯文本
10.035530102015 bits

Therefore:

纯文本
PASS_STATIC_CAPACITY_HARD_KILL_GATE

This is only a stress test; HElib capacity is not an additive bit-loss ledger.

7. Operation-count state

Baseline transform-side:

纯文本
5 forward
+ 5*(1 outer inverse + 13 Frobenius)
= 5 + 70
= 75 physical transform/key-switch calls

Current late-aggregation candidate:

纯文本
5 branch-local forward
+ 1 shared pure inverse outer
+ 17 shared pruned Frobenius
= 23

Canonical count:

纯文本
75 -> 23

Do NOT use stale 75 -> 19.

Shared reconstruction:

纯文本
5 -> 1

Recovery:

纯文本
70 -> 18 physical calls

Per selected leaf:

candidate recovery KS depth = 14;
stock one-branch recovery KS depth = 14.

Sibling-only Frobenius calls do not flow into another selected leaf's noise chain.

Candidate still pays:

five branch-local forward transforms;
five branch-local reLinearize-to-recrypt-key operations;
five rawModSwitch calls;
five newMakeDivisible/divide passes.

The count 23 is NOT total operations and NOT a latency prediction.

8. Latency/value state

Published external sanity baseline for p=5,w=512,k=5 Corr./TnM:

纯文本
SlotsToCtxts = 2.284 s
MultKey      = 4.732 s
CtxtsToSlots = 0.078 s
DigitExtract = 4.240 s
total        = 11.334 s
final capacity = 101
remaining multiplications ≈ 5

Published thin external sanity:

纯文本
latency ≈ 2.82 s
final capacity ≈ 151
remaining multiplications ≈ 8
throughput ≈ 107.06

Do not mix these absolute seconds with unrelated hardware for a strict verdict.

Turn 20 placement-specific Amdahl sanity model:

shareable MultKey pool =:

reconstruction 5 -> 1;
inverse/recovery 70 -> 18.

Five branch-local forward/nonlinear preprocess paths remain.

At zero incremental overhead, shareable MultKey fraction alpha required:

纯文本
10% whole-pipeline latency gain:
  29.94% -- 32.24%

20% gain:
  59.88% -- 64.49%

thin-throughput parity at C_new=101:
  50.19% -- 54.05%

Therefore static latency value is NOT killed, but wall-clock cannot be inferred from 75 -> 23.

Future measurement must use actual:

纯文本
T_candidate
  = T_baseline
    - S_core_actual
    + H_actual

where H_actual is the signed net delta of changed work.

9. Novelty state

Broad novelty is KILLED for:

batch bootstrapping via packing;
pack/unpack amortization in general;
one shared bootstrap for multiple ciphertexts;
generic partial CoeffToSlots;
“only recover useful coefficients”;
Geelen-style binary unpack recurrence;
Aung's broad repeated-MultKey objective;
generic HPS fractional CRT quotient / certified fallback.

Strong broad prior neighbors:

Geelen–Vercauteren batch bootstrapping via packing;
stock HElib packedRecrypt;
amortized bootstrapping literature.

Targeted search found NO exact collision for this narrow ordering:

纯文本
pre-tag identities
→ independently cross rawModSwitch/newMakeDivisible/divide
→ aggregate at first useful affine post-divide boundary
→ one reconstruction
→ target-pruned full-domain recovery

Current novelty label:

纯文本
NARROW / CONDITIONAL / NO EXACT COLLISION FOUND

Search absence is NOT novelty proof.

The elementary affine distributivity identity alone is too weak for a strong paper.

The defensible contribution package, only if native value survives, is:

纯文本
Aung repeated-MultKey bottleneck
→ prove naïve early fusion fails
→ identify rawModSwitch as decisive nonlinear boundary
→ preserve branch identity before it
→ delay aggregation to first common affine boundary
→ target-pruned full-domain recovery
→ material latency/Pareto improvement

Without a ≥10% end-to-end latency win or strict Pareto gain, publication value is likely weak.

10. Implementation contract

Pinned source target:

纯文本
homenc/HElib@acdb264

Do NOT expose:

PubKey::recryptEkey;
PubKey::recryptKeyID.

Do NOT make newMakeDivisible public.

Preferred minimal patch:

factor stock thin recryption preprocessing into an internal helper through /5, conceptually:

纯文本
preprocessThinToPostDivide(branch)
  -> {zz0, zz1}

It must reuse source-identical arithmetic:

纯文本
slotToCoeff
→ canonicalize/modDown
→ reLinearize(recryptKeyID)
→ rawModSwitch
→ stock raw-noise check
→ newMakeDivisible
→ /5

Then a narrow late-aggregation entry point:

纯文本
thinReCryptLateAggregate(out, taggedBranches)

internally:

纯文本
Z0 = Σ zz_i[0]
Z1 = Σ zz_i[1]

out = recryptEkey
out.multByConstant(Z1)
out.addConstant(Z0)

Return at temporary ptxtSpace=625.

Do NOT run stock coeffToSlot or extractDigitsThin inside this helper.

Candidate then runs:

pure power-basis inverse;
17-call pruned unpack;
four L0..L3 recombinations;
Aung Algorithm 4;
final original-intFactor restoration.

No evaluator secret-key access is introduced.

11. Future native correctness oracle for THIS candidate

Before timing, construct both:

Reference path:

纯文本
for each post-divide pair (z0_i,z1_i):
    R_i = recryptEkey
    R_i.multByConstant(z1_i)
    R_i.addConstant(z0_i)

R_ref = Σ_i R_i via Ctxt::addCtxt

Candidate path:

纯文本
Z0 = Σ_i z0_i
Z1 = Σ_i z1_i

R_fused = recryptEkey
R_fused.multByConstant(Z1)
R_fused.addConstant(Z0)

Require before performance interpretation:

same ptxtSpace = 625;
same intFactor;
same prime set;
same part handles;
corresponding DCRT ciphertext parts exact-equal modulo the common prime set;
decrypted temporary plaintexts equal modulo 625.

Do NOT require noiseBound or generic auxiliary bookkeeping equality.

Additional tagged-forward correctness-only checks:

before tag, verify each Aung branch slot is base-ring scalar in both physical slots;
after tag X^j, first physical slot = aX^j;
second physical slot = b rho(X^j);
after branch slotToCoeff, compare against exact full-forward algebra.

Any mismatch => FAIL_CORRECTNESS before timing.

12. Future timer / decision contract

The OLD pre-middle/shared-middle candidate timer contract is STALE.

For this late-placement candidate, stage timers should conceptually include:

纯文本
SlotsToCtxts

tag_mult_5
branch_slotToCoeff_total_5
branch_canonical_moddown_relin_total_5
branch_rawModSwitch_total_5
branch_makeDivisible_divide_total_5

postdivide_Z0_Z1_accumulate
shared_recryptEkey_reconstruct_1

pure_inverse_1
pruned_unpack_17
L0_L1_L2_L3_recombine
DigitExtract_Algorithm4

candidate_total

Baseline:

纯文本
SlotsToCtxts
five_branch_MultKey
CtxtsToSlots
DigitExtract
baseline_total

If possible, split baseline MultKey further into:

five forwards;
five preprocess/reconstruction portions;
five inverse/recovery portions.

Paired protocol:

纯文本
3 warmups per workflow
20 measured pairs
alternate AB/BA
same input ciphertext copy
same context / keys / caches
no key regeneration
primary statistic = median(T_candidate / T_baseline)
also report mean, p90, paired-ratio bootstrap 95% CI

Decision rules:

纯文本
FAIL_CORRECTNESS:
  any decrypt mismatch;
  any raw-mod noise-bound failure;
  any divide-by-5 failure;
  wrong ptxtSpace/intFactor;
  wrong selected-leaf ordering;
  wrong L0..L3 ordering.

KILL_CAPACITY:
  correctness passes but final bitCapacity < 70;
  or source-equivalent remaining-depth test collapses.

STRONG_PASS:
  correctness PASS;
  paired median latency ratio <= 0.80;
  paired-ratio 95% CI upper <= 0.90;
  remaining multiplications >= 5;
  throughput >= matched thin;
  no hidden resource/key increase.

VALUE_PASS:
  correctness PASS;
  paired median ratio <= 0.90;
  95% CI upper <= 1.00;
  remaining multiplications >= 5;
  throughput >= 10% above matched Corr./TnM.

PARETO_PASS:
  latency gain <10% but strict declared secondary-frontier gain
  in capacity/depth/key-memory/RSS under resource parity.

PARK:
  correctness passes;
  no >=10% latency gain;
  no strict secondary-frontier gain.

FAIL_VALUE:
  candidate slower than matched baseline;
  no compensating Pareto improvement.
13. Resource parity

Under the pinned FULL Frobenius setup:

no new evaluation-key TYPE is required;
the 13 split exponents are from the already available Frobenius family;
monomial tags are public unit constants;
the existing recryptEkey is reused.

If the comparator instead uses reduced BSGS/MIN Frobenius resources, either:

load equivalent direct keys for both workflows; or
charge their cost/bytes to the candidate.

Always record:

serialized evaluation/public-key bytes;
candidate constant-table bytes;
candidate-only caches;
peak RSS.
14. Explicit stale-state blacklist

Do NOT propagate any of these as current candidate facts:

纯文本
current transform count = 19
one shared forward transform
pre-middle sum of five tagged branches
pre-middle sparse-packing factor-5 tax
branch labelling [3,0,2,1,4]
net public delta 2.016729 bits
generic ThinEvalMap correctness on arbitrary extension-valued inputs
exact equality to five stock CoeffToSlots transcripts
HPS carry kernel required by current candidate
old pre-middle/shared-middle timer contract

Current replacements:

纯文本
transform count = 23
five branch-local forwards
late factor-5 worst-case envelope only
branch labelling = [2,0,3,1,4]
late/four-output envelope = 2.164329587598 bits
ThinEvalMap exact only on globally tagged source-scalar subclass
target = correct five scalar lifts + Aung L0..L3 interface
HPS carry path secondary only
Turn-22 late-placement native contract
15. Session artifacts / SHAs

Key recovery artifacts from the completed session:

纯文本
/mnt/data/boot-r18-pretag-postdivide-affine-aggregation-gate.md
SHA256 54c73298149693bc64bfb543c1457a4c7c8a932bdf97fcaf57a8e9f90f32d0a1

/mnt/data/boot-r19-late-aggregation-noise-capacity-gate.md
SHA256 f0dc2b694706984d8f7edb34e7436bb478f03c54fd2c1e3ff1bde270f9929a05

/mnt/data/boot-r20-late-aggregation-latency-viability-gate.md
SHA256 11be6952df23483c710271b9c4ca4627a28490e15aac8d9338ae6d587891dd24

/mnt/data/boot-r21-late-aggregation-prior-art-collision-gate.md
SHA256 a90f4de4087363df21bd1522bfb27f24a6b88a4f9ad5fa4de892b21bd6aab710

/mnt/data/boot-r22-late-aggregation-implementation-preregistration-gate.md
SHA256 2e752fd6151917b1088606b2af315c5eb1a81ccbc49b98eb879614cdf2867f6d

/mnt/data/boot-r23-tagged-branch-thinevalmap-typing-gate.md
SHA256 087e9750eb993bf309cc0b035a01570d085801c2caf0d285a971ddf34afbf1cc

/mnt/data/boot-r24-late-aggregation-milestone-consistency-gate.md
SHA256 d82a1172aa0197a57a144d14d924c69f5a29be9008cba1f95c8c4692ef95ad33

/mnt/data/boot-r25-bgv-hidden-scale-reconstruction-linearity-gate.md
SHA256 e3d073b0f2351de6637187d22b813e7e79901c3da4d857270917554072407325

Latest durable Git checkpoint:

纯文本
bc0fab910d1ca741741afc4d1cb3912204e2c047

Do not claim the /mnt/data artifacts themselves are durable Git objects unless independently verified.

16. Latest Codex/native evidence already delivered

There is one durable Codex task record carried by the orchestrator.

It is HISTORICAL/INERT for execution purposes: current_status is COMPLETED, result was delivered, and it MUST NOT be restarted, duplicated, resubmitted, or silently repurposed.

Full required provenance:

JSON
{
  "task_id": "BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01",
  "origin_session_id": "1f28610c-0aa3-4cce-9ec9-158d114c5ae8",
  "origin_session": "密码学 17.0",
  "origin_turn": 4,
  "original_hypothesis": "TASK_ID: BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01 — Research Turn 4/25 paired same-machine throughput gate. Contract compared vanilla HElib thin, source-faithful Aung Corr./TnM, and the then-current post-raw fusion candidate under same HElib acdb264 environment/key resources. Correctness failure preempted timing. Full original hypothesis remains in orchestrator.db.",
  "working_directory": "/Users/bingwu/Developer/research-orchestrator",
  "execution_backend": "Codex CLI / codex exec",
  "model": "gpt-5.6-sol",
  "reasoning": "medium",
  "pid_or_remote_execution_identity": "54891",
  "start_time": "2026-10-31T19:00:21.095Z",
  "current_status": "COMPLETED",
  "expected_artifacts": [],
  "evidence_status": "AVAILABLE",
  "audit_status": "DELIVERED",
  "result_delivered": true,
  "do_not_rerun": true,
  "commit": "4326551c9825f719414e094935ec1db554f0c6fc"
}

Delivered result:

纯文本
FAIL_NATIVE_CORRECTNESS

- vanilla thin correctness PASS;
- source-faithful Aung Corr./TnM failed its first smoke correctness check;
- contract stopped immediately;
- candidate was NOT executed;
- no performance/capacity/CI/throughput verdict was produced;
- no scientific failure of the candidate was established;
- RM10/joint physical-hop audit was not reached;
- exact 741 MiB keyset was persisted;
- do not repeat the ~5.5 hour key generation.

Evidence references from the delivered task:

纯文本
/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-run.log

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-progress.jsonl

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/source/benchmark.cpp

Durable evidence reference:

纯文本
orchestrator.db codex_tasks.task_id=BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

This task remains background provenance only. It must NOT be restarted or duplicated.

Most importantly:

纯文本
THIS COMPLETED TASK DID NOT TEST THE NEW TURN-18 LATE-AGGREGATION CANDIDATE.

Do not reinterpret its FAIL_NATIVE_CORRECTNESS as a verdict on the new candidate.

17. Cross-session Codex/native lifecycle rules

Codex/native task lifecycle is independent of Research GPT sessions.

Rules:

pending tasks may cross session boundaries;
never rerun, duplicate, or resubmit an existing task;
never modify its working directory, source, binary, or artifacts while pending/inert;
no session-local turn is reserved for a pending task;
when a result becomes ready, the orchestrator delivers it to the latest active session;
that result preempts the next free substantive research turn for independent audit;
do not treat an undelivered result as known;
do not infer candidate identity from task name alone;
verify task provenance before applying a result to the current canonical candidate.

Authorized cheapest-decisive Codex execution does not require separate per-task PI approval when a native slot is genuinely free and the experiment has been properly preregistered.

Never start a second heavy native task while another authorized task occupies the local slot.

18. What to do next in 密码学 22.0

This completed session exhausted its 25 substantive turns, but the top-level BOOT frontier is NOT exhausted.

The new late-aggregation candidate is:

纯文本
STATICALLY READY
NO KNOWN CHEAP SOURCE-SEMANTIC BLOCKER
NATIVE CORRECTNESS/VALUE UNMEASURED

The successor should first restore this canonical state and check the current orchestrator/native-slot status.

If no newly delivered native result preempts the turn, choose ONE new cheapest-decisive BOOT research unit.

Highest-value directions include, in order of evidence gain:

Verify whether the existing persisted 741 MiB keyset / comparator harness can support a clean future implementation of the NEW late-placement candidate without repeating key generation, while keeping the old completed task untouched.

Source-audit and design the smallest possible correctness-only implementation diff for:

preprocessThinToPostDivide;
exact post-divide pair summation;
one reconstruction;
exact part-equality oracle.
Do not launch heavy native work until the native slot is free.

If a native slot is free and the new candidate contract is source-ready, the next decisive native gate should test the NEW late-placement candidate, not resurrect the old post-raw candidate.

If implementation readiness is blocked, prescout another BOOT bottleneck rather than spending turns on low-value repetition.

The candidate/family soft/hard substantive-turn budgets remain:

纯文本
soft: 8
hard: 12

Use them as guidance, not as an excuse to stop useful falsification prematurely.

19. PI / strategy rules

Human PI decides:

final research direction;
publication strategy;
acceptable assumptions/tradeoffs;
whether a narrow contribution is worth pursuing;
major irreversible pivots.

Agent may autonomously:

search literature;
audit source;
derive theorems/counterexamples;
perform cheap static tests;
design reproducibility contracts;
launch already-authorized cheapest-decisive Codex execution when the native slot is free.

Do not WAIT_PI merely because:

one candidate failed;
a family was parked;
a PI decision is inherited;
native work is temporarily unavailable.

WAIT_PI/STOP only when the top-level BOOT frontier is exhausted, and explicitly state:

纯文本
research_frontier_exhausted: true
20. Strict ORCHESTRATOR_CONTROL protocol for every normal successor answer

Every normal substantive research answer in 密码学 22.0 MUST end with exactly one control block of this form:

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

another independent research step is available;
no native execution is being launched in that answer.
EXECUTE

Use only when:

a specific cheapest-decisive Codex/native task is actually being authorized/launched;
the native slot is free;
the task has an explicitly established task_id.

Then include inside the same block:

纯文本
task_id: <EXPLICIT_TASK_ID>

Never invent a task_id after the fact.

WAIT_PI

Allowed only when:

the current issue genuinely requires PI judgment;
AND no independent reversible research remains.

For WAIT_PI, the block MUST additionally include:

纯文本
research_frontier_exhausted: true

unless the wait is for a PI-only top-level strategic choice while the entire BOOT frontier is genuinely exhausted.

If requires_pi: true, independent_research_available MUST always be present and accurate.

STOP

Allowed only when:

the top-level research objective is exhausted or decisively closed.

The block MUST include:

纯文本
research_frontier_exhausted: true
Additional control rules
milestone: true only for a material durable checkpoint/result.
requires_pi: false for ordinary autonomous research.
independent_research_available: true whenever another no-regret in-scope step exists.
Never use EXECUTE while another heavy native task occupies the slot.
Never place prose after the ORCHESTRATOR_CONTROL block.
Do not emit an ORCHESTRATOR_CONTROL block for a future HANDOFF-ONLY turn when the controller explicitly requests the special two-block handoff format instead.
21. Final transferred state
纯文本
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

LATEST_COMPLETED:
Research Turn 25/25 — BGV hidden-scaling / exact reconstruction-linearity gate

LATEST_VERDICTS:
PASS_BGV_HIDDEN_SCALE_RECONSTRUCTION_LINEARITY
PASS_EXACT_CIPHERTEXT_PART_LATE_AGGREGATION_EQUIVALENCE
PASS_NO_BRANCH_INTFACTOR_HARMONIZATION
REFINE_LATE_SUM_NOISE_FACTOR5_AS_WORST_CASE_NOT_MANDATORY

PRIMARY_CANDIDATE:
PRE-TAG + POST-DIVIDE LATE AGGREGATION

STATIC_STATUS:
READY / NO KNOWN CHEAP SOURCE-SEMANTIC BLOCKER

TRANSFORM_LEDGER:
75 -> 23

RECONSTRUCTION:
5 -> 1

RECOVERY:
70 -> 18

FINAL_BRANCH_LABELLING:
[2,0,3,1,4]

PESSIMISTIC_STRESS_CAPACITY:
79.881474102015 bits

STATIC_HARD_KILL:
69.845944 bits

NOVELTY:
NARROW / CONDITIONAL / NO EXACT COLLISION FOUND

NATIVE_VERDICT_FOR_NEW LATE-PLACEMENT CANDIDATE:
NONE / UNMEASURED

DURABLE_GIT_CHECKPOINT:
bc0fab910d1ca741741afc4d1cb3912204e2c047

PENDING_PI_DECISIONS:
none

RESEARCH_FRONTIER_EXHAUSTED:
false

CONTINUOUS_AUTONOMOUS_RESEARCH:
enabled
