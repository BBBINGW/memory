# 密码学 15.0 handoff

Resume research — Session Handoff

This is the successor to the completed ordinary-Chat BOOT research session 密码学 14.0. It is the SAME logical BOOT research program, not a new topic.

0. Required research identity

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

LATEST_COMPLETED:
Research Turn 25/25 — MULTIOUTPUT_HOISTED_LINEAR_TRANSFORM_GATE

CURRENT_STATUS:
SESSION_RESEARCH_COMPLETE / CONTINUOUS_AUTONOMOUS_RESEARCH

NEXT_ITERATION:
Resume from this handoff and autonomously choose the next cheapest decisive BOOT test. Do not continue local RMFE single-linear-phase micro-optimizations merely because they were the latest topic.

NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false

PENDING_PI_DECISIONS: none

PENDING_CODEX_TASKS_MAY_CROSS_SESSION_BOUNDARIES: true

1. Durable authority

Primary research-memory interface:
GitHub Notes / BBBINGW/memory.

The session read-before-write checkpoint succeeded at:

591364e4810bff8d1cf5bc396b815b564d47377c

Treat this checkpoint as the authoritative session handoff state.

At session start, first restore the latest BOOT durable state from GitHub memory, beginning with:

findings/boot-STATE.md
findings/boot-s2-nonfrobenius-basis-lower-bound-gate-2026-10-30.md
findings/boot-multioutput-hoisted-linear-transform-gate-2026-10-30.md
any handoff/checkpoint material committed at or before main@591364e4810bff8d1cf5bc396b815b564d47377c
earlier RMFE findings referenced by the BOOT state

GitHub Notes has been intermittently unhealthy. If connector reads fail, do NOT stop research merely for that reason. Use verified Git authority and do not claim connector-derived facts that were not actually read.

Important durable commits created during the final two turns:

Turn 24 finding:

path: findings/boot-s2-nonfrobenius-basis-lower-bound-gate-2026-10-30.md
commit: 58ea2675421b99a8d1aae5934dc4219c76ab4f38
blob SHA: 9d390d66fc2d27def9b90400b70f2cdec1379e1a

Turn 25 finding:

path: findings/boot-multioutput-hoisted-linear-transform-gate-2026-10-30.md
commit: 881a4b137c3bba497fce8945814321ca387b46c0
blob SHA: 570129f43af8cfacc1744af997282403f35a338e

The later session checkpoint main@591364e4810bff8d1cf5bc396b815b564d47377c supersedes these individual commits as the session-level authority.

Do not let stale global STATE.md material for other tracks override the current explicit BOOT identity.

2. Research governance

CONTINUOUS_AUTONOMOUS_RESEARCH=true.

Within the PI-authorized top-level BOOT objective:

per-iteration PI authorization is NOT required;
authorized cheapest-decisive Codex work does NOT require separate per-task PI approval;
candidate substantive-turn budget is soft 8 / hard 12;
a failed candidate/family must be park/kill + autonomous in-scope reprioritization;
do NOT WAIT_PI merely because one candidate fails;
PENDING_PI_DECISION is a durable advisory queue, not automatically blocking;
if a pending PI decision exists but independent reversible work remains, continue that work;
WAIT_PI/STOP is permitted only when the entire authorized top-level BOOT research frontier is exhausted;
WAIT_PI/STOP must explicitly include:
research_frontier_exhausted: true
reversible AI_PROVISIONAL_CHOICE is provisional and never final PI approval.

Research philosophy:

smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted

Human/PI:

strategic importance;
final direction;
publication/contribution judgment;
irreversible assumption/trade-off decisions.

Research GPT:

retrieval;
source/paper audit;
derivation;
counterexamples;
falsification;
cheapest decisive experiments;
evidence/provenance audit;
autonomous reversible reprioritization inside BOOT.

Never promote one bounded PASS into full correctness, DFR, security, end-to-end speedup, or publication contribution.

3. Session accomplishments — 密码学 14.0

The session completed Research Turns 1–25.

The final research arc audited the RMFE “single linear phase” family around Aung et al. PKC 2025 / ePrint 2025/350.

High-level background already established before the final turns:

Aung et al. explicitly list “Do one linear phase instead of multiple” as future work.
Therefore HIGH_LEVEL_SINGLE_LINEAR_PHASE_NOVELTY = KILLED.
Only a specific new mechanism could still be contribution-bearing.
Earlier merged-before-rounding / one-core variants failed because nonlinear ModSwitch rounding does not commute with RMFE decoding and causes p-adic/carry amplification.
R24 source-r1 one-core native path was classified FAIL_ONECORE_PADIC_SEMANTICS; this is not a universal impossibility, but that concrete route is killed/parked.
R16/native decoder conditioning showed very large HElib coefficient-domain projection-mask norms.
Subsequent turns tested whether alternate RMFE representation choices could rescue this.
Turn 20–24 representation/conditioning sequence

s=2 RMFE was the strongest representation-level rescue candidate because Aung’s legality bound permits:

p=5, eta=125, k=5, s=2, w=512,
with sw=1024 | 8192.

Natural tensor-basis conditioning looked good internally, but the real HElib cyclotomic embedding largely destroyed that benefit.

Turn 21:
S2_HELIB_EMBEDDING_CONDITIONING_GATE

native embedding reduced the apparent internal-basis gain to roughly:
L1 improvement ≈2.25x
L2 improvement ≈1.75x
insufficient for the p-adic rounding obstruction.
order-3 s=2 interpolation candidate parked/killed.

Turn 22:
S2_NATIVE_POINTSET_EXHAUSTIVE_GATE

exhaustive Teichmüller point-set search did not approach the required 10x conditioning gate.
best native point-set improvement remained only ~2x-scale.
point-set conditioning rescue killed.

Turn 23:
S2_TARGET_GENERATOR_FROBENIUS_INVARIANCE_GATE

replacing target generator by any G-Frobenius conjugate applies a signed permutation automorphism in the HElib coefficient basis;
L1/L2/Linf are exactly invariant;
Frobenius-generator rescue killed.

Turn 24:
S2_NONFROBENIUS_BASIS_LOWER_BOUND_GATE
Result:
FAIL_AFFINE_KUMMER_BASIS_RESCUE
GENERAL_DENSE_NONAFFINE_BASIS = UNCLEAR

Exact exhaustive screen:

G=GR(625,2)
|G|=625^2=390625 lifted points
both physical-slot orientations
exact legality via distinct F25 residue classes

Best legal five-point configuration:

representative set: {infinity, 0, 24, 26, 2}
worst L1 = 78303
worst L2 ≈4038.264354893077
worst Linf = 312

R16 baseline:

L1 = 263853
L2 = 8249.83
Linf = 312

Improvement:

L1 ≈3.3696x
L2 ≈2.0429x

Required 10x L1 threshold:

<26385.3

Remaining shortfall:

78303 / 26385.3 ≈2.97x

The exhaustive lifted-point screen also closes the natural sparse non-Frobenius affine/Kummer generator family:

zeta = a + c alpha^r,
a in G,
c in G^×,
gcd(r,512)=1.

Reason:

affine shift/scale maps interpolation points bijectively within G and is already covered by the full lifted-point enumeration;
odd Kummer exponent r only signed-permutes the native coefficient support/norms.

Disposition:

Teichmüller point choice: KILL
arbitrary lifted G-point choice: FAIL 10x gate
Frobenius generator conjugation: KILL
affine shift/scale: KILL
non-Frobenius Kummer exponent: KILL
genuinely dense non-affine generator f(alpha): UNCLEAR / PARK
S2 conditioning rescue: PARK

No native experiment is justified for this branch.

4. Final Turn 25 — MULTIOUTPUT_HOISTED_LINEAR_TRANSFORM_GATE

Primary question:

Can the five RMFE thin branches share expensive HElib SlotsToCoeff/CoeffToSlots automorphism/key-switch decomposition work through multi-output hoisting, without merging ciphertexts and without changing the secret/evaluation-key assumption?

Verdict:

FAIL_STOCK_CROSS_BRANCH_HOIST

Natural common-source weighted-transform rescue:

COST_NEGATIVE_AT_K5

Pinned source:
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

Key source fact:

BasicAutomorphPrecon is explicitly a precomputation for many automorphisms of THE SAME ciphertext.

It executes:

ctxt.parts[1].breakIntoDigits(polyDigits)

and caches those ciphertext-specific gadget digits.

Therefore:

the expensive hoisted decomposition is ciphertext-dependent;
it is not a key-only cache;
it cannot be reused directly across five distinct branch ciphertext states.
Exact ThinEvalMap geometry

m=32768
p=5
phi(m)=16384
ord_m(5)=8192
physical slots=2

Current mvec is effectively:
[32768]

Thus explicit ThinEvalMap dimension:

D = 16384 / 8192 = 2.

Therefore:

SlotsToCoeff explicit MatMul is only a 2x2 transform;
at most one nontrivial slot automorphism per branch;
perfect sharing across five branches can only reduce 5 calls to 1, saving 4.

CoeffToSlots for invert=true is:

2x2 MatMul
→ traceMap

The dominant extra operation is traceMap.

Exact trace structure

traceMap uses:

d = ord_m(5) = 8192 = 2^13.

For the non-MIN path audited in pinned HElib, binary doubling gives exactly 13 Frobenius automorphism calls per branch.

Five branches:

5 * 13 = 65

branch-local trace automorphisms.

Each trace evolves a different branch ciphertext accumulator, so stock hoisting cannot share the cached gadget decomposition.

Common recryptEkey rescue

Post-ModSwitch branch:

u_i = z0_i + z1_i * E_s

where E_s is the common encrypted boot secret.

The D=2 map can in principle share one automorphism of E_s and save a small constant.

But:

Tr(u_i)

Tr(z0_i)
+
sum_{j=0}^{8191} sigma^j(z1_i) sigma^j(E_s)

with branch-specific z1_i.

If rewritten as one common-source transform of E_s, the all-ones structured trace recurrence is lost and becomes a generic weighted 8192-term linear transform.

Standard BSGS scale:

~2 sqrt(8192) ≈181 automorphisms.

Baseline five structured traces:

65 automorphisms.

Thus the natural common-source rescue is cost-negative for k=5.

Transform-side optimistic ceiling

Approximate automorphism accounting:

baseline:

SlotsToCoeff D=2: 5
CoeffToSlots D=2: 5
trace: 65
total: 75

best cheap sharing while preserving short trace:

shared SlotsToCoeff D=2: 1
shared CoeffToSlots D=2: 1
trace remains branch-local: 65
total: 67

Optimistic reduction:
75 → 67 ≈10.7%

This is nowhere near k-fold collapse and ignores plumbing/ct-pt accumulation overhead.

Projection side also showed no meaningful automorphism-count gain:

five degree-512 structured traces: 5*9 =45
generic common-source BSGS over 512 positions: ~45

Therefore:

stock cross-branch ThinEvalMap hoisting: KILL
generic common-source weighted trace at k=5: KILL/PARK on cost
small D=2 reuse: engineering-only
no native/Codex experiment justified
5. Current scientific interpretation

The RMFE single-linear-phase local-rescue family has been heavily screened.

Killed/parked routes include:

merged-before-rounding one-core path
direct stock raw merge
R16 decoder-conditioning rescue
s=2 Teichmüller point-set rescue
arbitrary lifted-point rescue
Frobenius target-generator rescue
affine/Kummer non-Frobenius generator rescue
stock cross-branch HElib hoisting
generic common-source weighted-trace rescue at k=5

Still UNCLEAR but low-priority:

genuinely dense non-affine target generators
substantially changed ring/secret/evaluation-key representations

These are not recommended as the next turn because they are high-cost and lack positive signal.

The useful conceptual result accumulated across the session is:

merge-before-rounding fails because nonlinear rounding does not commute with RMFE decoding / projection;
better internal RMFE conditioning does not automatically survive the concrete HElib cyclotomic coefficient embedding;
stock HElib hoisting amortizes many automorphisms of one ciphertext, not the same transform across distinct branch ciphertexts;
forcing common-source representation can destroy logarithmic trace structure and become more expensive than branch-local execution.

Do not continue local RMFE single-linear-phase micro-optimization by inertia.

6. Strongest candidate / main hypothesis entering 密码学 15.0

There is currently NO validated strongest candidate inside the local RMFE single-linear-phase family.

The top-level BOOT research frontier is NOT exhausted.

Strongest strategic state:

RMFE_SINGLE_LINEAR_PHASE_LOCAL_RESCUE_FAMILY:
HEAVILY_SCREENED / MOST_LOW_REGRET_VARIANTS_KILLED_OR_PARKED

TOP_LEVEL_BOOT:
OPEN

Do not invent a new paper-level hypothesis in the handoff.

The successor's first substantive turn should autonomously reprioritize within BOOT and choose exactly one genuinely different bottleneck/mechanism using the usual smallest-falsifier rule.

The successor should first restore the authoritative BOOT state and inspect surviving BOOT branches / open problems before selecting that hypothesis.

Do not automatically return to:

decoder conditioning;
exotic RMFE basis search;
same-ring envelope;
cross-branch ThinEvalMap hoisting.
7. Latest native / Codex evidence

No new native or Codex experiment was launched for Turns 24–25.

Latest final-turn conclusions are source/algebra/cost audits only.

No native experiment is justified for:

S2 conditioning rescue;
multi-output hoisted linear-transform branch.

PENDING_CODEX_TASKS:
None.

There are no pending tasks to reserve an audit turn for.

If future sessions launch background Codex/native work, task lifecycle is independent of the Research GPT session:

do not wait merely because a task is pending;
do not restart or duplicate it;
do not reserve a local turn for it;
when the orchestrator delivers a result to the latest active session, audit it on that session's next free substantive turn.

PENDING_CODEX_TASKS_MAY_CROSS_SESSION_BOUNDARIES: true.

For this handoff specifically:
there are NO pending task records to carry.

8. Codex delegation rules

Codex execution is allowed autonomously only when it is the cheapest decisive test inside the authorized BOOT objective.

Before delegation:

define one falsifiable hypothesis;
define one bounded test;
pin source/revision/parameters;
define exact PASS/FAIL criteria;
prohibit parameter sweeps and opportunistic rescues unless explicitly part of the hypothesis.

Do not:

rerun completed tasks;
duplicate background tasks;
silently broaden scope;
infer native results that were not delivered;
claim DFR/security/end-to-end speedup from one correctness test.

Native-heavy work should only follow a surviving static/source gate.

9. Persistence rules

GitHub Notes is the primary research-memory interface.

For durable scientific results:

read-before-write;
write a dedicated finding;
verify the persisted content / commit;
update BOOT state only after successful verification.

If GitHub Notes is unavailable:

use verified Git authority;
do not stop research solely because of connector failure;
do not claim persistence unless commit/write/readback was actually verified.

The latest session checkpoint is:

591364e4810bff8d1cf5bc396b815b564d47377c

10. Strict normal-answer ORCHESTRATOR_CONTROL protocol

Every normal substantive research answer in 密码学 15.0 must end with exactly one control block:

<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

If action=EXECUTE and a task identifier was explicitly established, include:

task_id: <exact task id>

inside the block.

Rules:

CONTINUE

use when research can proceed autonomously without launching a delegated execution now.

EXECUTE

use only when the answer actually authorizes/launches a concrete execution task.

WAIT_PI

only if no independent no-regret research remains and a PI decision is genuinely required.
must include:
research_frontier_exhausted: true

STOP

only if the authorized top-level BOOT frontier is exhausted.
must include:
research_frontier_exhausted: true

If requires_pi: true, always include:
independent_research_available: true | false

A pending PI advisory does not automatically imply WAIT_PI.

If:
pending PI decision + independent work available
=> CONTINUE.

If:
pending PI decision + no independent work available
=> WAIT_PI.

Never use WAIT_PI merely because one candidate or family failed.

Exception:
If the user explicitly requests "substantive research body only" and says the Orchestrator will separately request the control envelope, omit the control block in that answer. When the subsequent control-repair request arrives, output only the control block and nothing else.

11. Start-of-session instruction for 密码学 15.0

At the beginning of the new session:

Restore GitHub memory at main@591364e4810bff8d1cf5bc396b815b564d47377c.
Confirm:
TRACK_ID=BOOT
ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED=Research Turn 25/25 — MULTIOUTPUT_HOISTED_LINEAR_TRANSFORM_GATE
Confirm no pending Codex/native tasks.
Treat the RMFE local single-linear-phase rescue family as heavily screened, not as the automatic next candidate.
Select exactly ONE genuinely different BOOT bottleneck/mechanism with the highest expected information gain.
State one primary hypothesis and one cheapest decisive falsifier.
Continue autonomously; no per-turn PI authorization is required.
Persist any durable result with read-before-write and verified write-back.
