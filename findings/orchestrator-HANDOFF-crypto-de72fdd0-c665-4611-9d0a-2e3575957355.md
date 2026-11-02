# 密码学 23.0 handoff

Resume research — Session Handoff

You are the formal Research GPT continuing the same BOOT research program in a NEW ordinary Chat session. This is a session handoff, not a new project. Preserve all durable scientific state below exactly unless new evidence later supersedes it.

Identity / operating mode
Model provenance expected by PI: GPT-5.6 Sol / highest available reasoning effort.
ZERO_API_BILLING=YES.
GitHub Notes is the primary research-memory interface.
At the beginning of each substantive research iteration, recover relevant durable context first.
For every durable scientific result: read-before-write, persist to GitHub memory findings, then verify persistence.
If GitHub Notes is unhealthy, use verified local Git authority; connector failure alone must NEVER stop research.
CONTINUOUS_AUTONOMOUS_RESEARCH remains enabled.
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false.
Do not ask for per-turn PI authorization for reversible, in-scope work.
PENDING_PI_DECISION is an advisory durable queue, not automatically blocking.
WAIT_PI/STOP is valid only when the whole top-level research frontier is exhausted and must explicitly state research_frontier_exhausted: true.
Session identity

TRACK_ID: BOOT

ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

PREVIOUS SESSION: 密码学 22.0

NEW SESSION: 密码学 23.0

LATEST_COMPLETED:
Research Turn 25/25 — end-to-end static correctness closure audit

CURRENT_STATUS:
SESSION_RESEARCH_COMPLETE for the previous session.
The successor session may begin a fresh session-local substantive turn counter while preserving this same logical paper candidate and all scientific state.

PHASE:
CORRECTNESS_GATE

Durable session checkpoint

The read-before-write session handoff checkpoint succeeded at:

04dd5e03e17d7c69fb3bcbd253351418637dc29c

This is the authoritative handoff checkpoint supplied by the Session Controller.

Latest Turn-25 scientific finding before the handoff:

path:
findings/boot-RMFE-postdivide-turn25-end-to-end-static-correctness-closure-2026-11-02.md
finding commit:
20e488dbd813ecdae210a2a9cdc2706cc298b9e6
blob SHA:
6885ab59af403b71e0fdbc91d8e2b139fbf6a93c

Turn-24 modulus-bridge finding:

path:
findings/boot-RMFE-postdivide-turn24-forward-mod5-z625-lift-bridge-gate-2026-11-02.md
finding commit:
22d50cad999b90f8163c241b95dc9c390faac645
blob SHA:
1903cfb6d76647d487c56bfa12145e4a03b90b70

Frozen revised recovery-only canary source:

path:
findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt
blob SHA:
6ae4bc7e48e0390f8dec97429f4ddb89565928c0

Pinned HElib source:

homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

Research philosophy

Default research discipline:

纯文本
smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted

Each substantive iteration must contain exactly:

纯文本
one primary hypothesis
+
one minimal decisive test

Every test must reduce a named uncertainty for the complete active PAPER_CANDIDATE. Local PASS/FAIL accumulation is not progress by itself.

Paper path:

纯文本
Important Problem
→ Novelty Preflight
→ Constructive Design
→ Complete Correctness
→ Security
→ Scientific Value
→ Independent Audit
→ Paper Contribution

Native evidence order is mandatory:

纯文本
1. Source audit
2. Small correctness canary
3. Exact parameter/interface verification
4. Complete baseline correctness
5. Candidate correctness
6. Noise/security compatibility
7. Matched benchmark
8. Independent raw audit

Do not skip prerequisites and do not infer pending evidence.

PASS_TOY / PASS_STATIC / PASS_MATH do not imply PAPER_READY.

No performance verdict before baseline correctness and matched candidate correctness.

Previous-session accomplishments

Research Turns 1–25 are complete. Do NOT regenerate or recount them.

The previous session progressively closed the CURRENT candidate's static source/mathematical correctness interfaces, including:

recovery-only canary source contract;
source-faithful branch-local middle;
exact post-divide aggregation placement;
one shared recryptEkey reconstruction;
pure normal_basis=false Z625 EvalMap inverse;
scalar-unit normalization by 28;
standard-keyset parity for the pure inverse;
source-faithful SlotsToCtxts common ptxtSpace=5 / common f_in;
source guarantee that each physical SlotsToCtxts slot is actually a Z5 scalar;
final Recode at ptxtSpace=5 with existing 625-typed key-switch matrices;
exact shared-reconstruction ciphertext-part/metadata equivalence;
Algorithm-4 factor67 5-adic-unit closure;
correction of the forward-modulus theorem from an overstrong Z625 claim to the actual Z5 forward plus arbitrary-Z625 lift bridge;
final end-to-end static typed dependency audit;
proof that the two physical SIMD slots may use independent arbitrary Z625 lift vectors;
reinterpretation of public443 as a mod-5 residue-unit correction rather than requiring exact lifted rho/182 coherence.
Latest Turn-25 primary hypothesis

After all Turn16–24 revisions, does the CURRENT candidate form one complete static correctness chain with no unidentified semantic/type edge, so that the only remaining blockers are native evidence-order blockers rather than another missing theorem/source contract?

Verdict:

PASS at MATH/STATIC level

Exact latest durable markers:

纯文本
PASS_CROSS_SLOT_ARBITRARY_LIFT_INDEPENDENCE
PASS_RHO_RESIDUE_CORRECTION_WITH_PUBLIC_443
PASS_SLOTWISE_FOUR_CORRECTION_HANDOFF
PASS_CURRENT_END_TO_END_STATIC_TYPED_CORRECTNESS_CLOSURE
PASS_NO_IDENTIFIED_STATIC_SEMANTIC_EDGE_GAP

SUPERSEDE_EXACT_LIFTED_RHO_COHERENCE_REQUIREMENT
SUPERSEDE_STALE_TRANSFORM_COUNT_19_WITH_23

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

Interpretation:

Static theorem closure is conditional and DOES NOT equal complete candidate correctness.

Canonical CURRENT construction

Fixed parameters:

纯文本
p = 5
m = 32768
w = 512
k = 5
r = 1
e = 4
e' = 1
q = 626
temporary ptxtSpace = 625
local extension degree d = 8192
eta = 125

Canonical coordinate set:

纯文本
J = [0,1024,7168,2048,6144]
  = {0,+1024,-1024,+2048,-2048} mod 8192

Final branch labels in J order:

纯文本
[2,0,3,1,4]

Canonical path:

纯文本
Aung SlotsToCtxts
  ptxtSpace = 5
  five thin scalar branches
  common source f_in
→ global monomial tag on EACH branch
→ EACH branch:
     stock thin pre-forward level prep
     dropSmallAndSpecialPrimes
     bringToSet(first <= 3 ctxt primes)
     tagged ThinEvalMap forward at application ptxtSpace=5
     canonicalize/modDown
     reLinearize(recryptKeyID)
     rawModSwitch(q=626)
     source branch-local bounds/checks
     newMakeDivisible(5)
     exact integer divide by 5
→ five exact ZZX pairs
→ Z0 = Σ z0_i
→ Z1 = Σ z1_i
→ ONE shared recryptEkey reconstruction
     ptxtSpace = 625
     intFactor = 1
     keyID = 0
→ pure:
     EvalMap(*rcData.ea,
             false,
             rcData.mvec,
             true,
             rcData.build_cache,
             false)
→ semantic scalar-unit normalization:
     multByConstant(28L)
     factor 1 → 67
     no direct parts/noise multiplication
→ target-pruned full-domain recovery
     17 physical Frobenius calls
→ five independently valid arbitrary Z625 branch lifts
     correct source residues mod 5
→ per-slot routing
→ public443 residue correction on nonzero second-slot targets
→ exact slotwise L0,L1,L2,L3
→ Aung Algorithm 4
     arbitrary Z625 lifts allowed
     six divideByP boundaries
     all dynamic factors remain 5-adic units
→ final Recode at ptxtSpace=5
→ restore saved source f_in
Critical modulus correction from Turn 24

DO NOT claim the actual tagged forward operates over Z625.

Actual source behavior:

纯文本
slotToCoeff = ThinEvalMap(context.getEA(), ..., invert=false)

so production branch forward is at:

纯文本
application r = 1
ptxtSpace = 5

Temporary Z625 appears only after recryptEkey reconstruction.

Correct theorem:

纯文本
tagged ThinForward is exact over Z5
→ branch-local recryption produces arbitrary Z625 lift
→ normal_basis=false Z625 inverse reduces mod5 to inverse FullForward5
→ selected coordinates are arbitrary Z625 lifts with correct source residues

Do not resurrect:

纯文本
actual tagged forward exact over Z625
Cross-slot lift theorem from Turn 25

The two physical SIMD slots do NOT need a common higher-5-adic lift.

For slot h independently:

纯文本
A^(h) = (a_1^(h),...,a_5^(h)) ∈ Z625^5
a_i^(h) mod5 = source branch scalar in that slot

Define independently:

纯文本
L_t^(h) = Σ_i a_i^(h) * phi(e_i)^(5^t)

Aung Algorithm4 applies slotwise.

No requirement:

纯文本
A^(0) = A^(1)

and no requirement that reconstructed higher-adic digits preserve exact lifted rho coherence.

For a nonzero second-slot target:

纯文本
b_tilde mod5 = 2*b
443 mod5 = 3
3*2 = 1 mod5

so:

纯文本
443 * b_tilde

is simply another arbitrary Z625 lift of b.

Correct rationale:

纯文本
public443 corrects the known mod-5 residue unit
and yields a valid arbitrary Z625 lift

NOT:

纯文本
public443 exactly undoes an exact lifted 182 relation
Factor state

After shared reconstruction:

纯文本
intFactor = 1

Pure inverse preserves factor1.

Then:

纯文本
multByConstant(28L)

uses the BGV scalar-unit metadata path.

Because:

纯文本
28^-1 mod625 = 67

Algorithm4 receives common initial factor:

纯文本
67

NOT 1.

Turn23 proves all subsequent Algorithm4 factors remain 5-adic units under:

ciphertext multiplication;
add/sub harmonization;
relinearization/modulus maintenance;
divideByP reduction.

Exact numeric factor trajectory remains runtime-state dependent.

Algorithm4 plaintext-space ladder

Six exact divide boundaries:

纯文本
B1: 625 -> 125
B2: 625 -> 125
B3: 125 -> 25
B4: 625 -> 125
B5: 125 -> 25
B6: 25  -> 5

Aung arbitrary-lift theorem applies to:

纯文本
a_i ∈ Z_{p^e} = Z625

No canonical / Teichmüller lift requirement.

Final Recode

At the end of Algorithm4:

纯文本
ptxtSpace = 5

Final Recode is the mod-5 reduction of:

纯文本
pi = phi o psi

Same automorphism schedule, public constants interpreted mod5.

Existing ptxtSpace625 KeySwitch matrices are correctness-compatible because HElib reduces plaintext spaces through:

纯文本
gcd(5,625) = 5

No candidate-specific mod5 key family.

Correct final sequence:

纯文本
Algorithm4 divide ladder
→ ptxtSpace 5
→ final Recode mod5
→ restore saved f_in
→ return

Never restore f_in before final Recode.

Public restoration:

纯文本
final.multByConstant(InvMod(f_in,5))
Reconstruction theorem

Let post-divide branch pairs be:

纯文本
(a0_i,a1_i)

and stored boot key ciphertext be E = recryptEkey.

Separate reconstruction:

纯文本
R_i = E*a1_i + a0_i

Shared:

纯文本
R_shared
  = E*(Σ a1_i) + Σ a0_i
  = Σ R_i

This equality is exact at ciphertext-parts level under the audited representation scaling.

There are NOT five independent recryptEkey encryption noises: each branch copies the same stored recryptEkey.

Shared metadata:

纯文本
ptxtSpace = 625
intFactor = 1
keyID = 0
primeSet = primeSet(E)

Exact canonical-norm envelope is no worse than the conservative sum of the five separate envelopes.

Software floating estimator relation remains a native assertion, not a theorem-level exact floating claim.

Recovery

Current recovery is full-domain and accepts arbitrary dirty extension state.

Normalization:

纯文本
8192 mod625 = 67
67^-1 mod625 = 28

Current pruned recovery:

纯文本
physical Frobenius calls = 17
distinct exponents =
4096,2048,1024,512,256,128,64,32,16,8,4,2,1

Natural selected coordinate order after current pruned schedule:

纯文本
[0,2048,6144,1024,7168]

Final routing must use the established coordinate metadata and branch reordering.

Do not confuse full-tree target positions with pruned output order.

Current transform-side structural count

The stale value 19 is forbidden.

Current candidate structural transform-side count:

纯文本
5 branch-local forward transforms
+ 1 pure inverse outer stage
+ 17 recovery Frobenius calls
= 23

This is NOT:

total operation count;
latency;
matched speedup.
Evaluation-key resource state

For current m=32768, mvec=[32768].

Current pure inverse consumes:

纯文本
outer dim 0:
  order 2
  stock default strategy happens to be FULL
  ptxtSpace 625

Frobenius dim -1:
  order 8192
  FULL
  ptxtSpace 625

Candidate pure-inverse evaluation-key TYPE delta:

纯文本
0

Candidate pure-inverse evaluation-key BYTE delta:

纯文本
0

under the same standard bootstrapping key object.

Do not generalize this to arbitrary parameter sets.

Noise / capacity state

Known:

monomial tags have canonical norm1;
branch-local source recryption checks remain per-branch;
exact shared reconstruction has a valid conservative envelope;
factor67 unit closure is correct;
selected-leaf recovery has known structural key-switch depth.

Unknown / pending:

actual recovery-canary capacity;
concrete shared reconstruction noiseBound;
exact Algorithm4 factor/harmonization trajectory;
final capacity;
DFR;
full native correctness.

No static capacity or benchmark claim should be promoted to a performance verdict.

Closest prior art / novelty state

Primary adjacent work:

Aung et al. PKC 2025 / ePrint 2025/350.
HElib stock thin recryption.
Geelen-style binary unpack is NOT novel.
Broad shared-bootstrap novelty is NOT the claim.

Narrow candidate novelty remains only a PREFLIGHT possibility around:

纯文本
obstruction
→ first legal post-nonlinear/post-divide merge
→ target-pruned recovery

Aung explicitly identifies avoiding repeated MultKey across split ciphertexts as future work.

NOVELTY_STATUS:

PREFLIGHT

Do not report CLEAR until independent prior-art audit passes.

Killed / parked / forbidden routes

Do NOT reopen without satisfying a durable reopening condition:

pre-raw / pre-newMakeDivisible aggregation;
direct aggregation through rawModSwitch;
generic aggregate-only recovery from five arbitrary dirty reconstructed branch states;
rank-5 dirty-state closure;
one shared forward over a pre-packed arbitrary extension state;
generic ThinEvalMap correctness on arbitrary extension values;
post-unpack exact lifted rho/182 coherence requirement;
stale Algorithm4 initial factor1;
stale transform-side count19;
stale branch labels [3,0,2,1,4];
post-global rho/443 extra compensation;
five separate x28 leaf multiplications;
production requirement to fold28 into a custom inverse;
extra mod5 Recode key family;
final Recode omission;
restoring f_in before final Recode.
Latest native / Codex evidence

No currently pending Codex/native task.

No native result is known.

Recovery-only canary:

NOT EXECUTED

Exact parameter/interface:

NOT EXECUTED

Matched source-faithful Aung baseline:

PENDING

Complete candidate native correctness:

PENDING

Do not infer PASS/FAIL from absence.

Previous available execution environment lacked HElib and NTL, so the frozen canary could not be compiled there. That infrastructure fact is not scientific evidence.

PENDING_CODEX_TASKS

None.

There are no background tasks to audit or wait for.

General cross-session rule still applies:

Pending native/Codex tasks may cross session boundaries.
A background task must never be restarted, resubmitted, duplicated, or modified merely because the Research GPT session changed.
When the orchestrator later delivers a ready result, audit it independently in the latest active session's next free substantive turn.
Do not reserve a session-local turn while a background task is merely pending.
Since PENDING_CODEX_TASKS is currently empty, no task provenance needs active polling.
Strongest candidate

CANDIDATE_ID:

legacy-484479fe4613

RANK:

1

STATUS:

ACTIVE

CONTRIBUTION_TYPE:

ALGORITHM

The candidate remains credible and has a decisive native correctness path.

No ranked backups are currently recorded.

Main current hypothesis

The fixed static construction is semantically coherent; the next scientific uncertainty is whether the frozen HElib recovery machinery actually executes correctly with the exact current interface and parameters.

Do NOT spend the next turn on another source micro-audit unless native evidence falsifies or exposes an unverified frozen interface.

NEXT_ITERATION

Successor session should choose the cheapest decisive evidence-order action.

Highest priority:

Run the frozen revised recovery-only canary against:

homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

with:

HELIB_DEBUG=ON

Acceptance must include the frozen canary oracle, including at least:

纯文本
scalar_unit_28=PASS
17 recovery Frobenius calls
exact routing
exact selected dirty lifts
exact L0,L1,L2,L3

If the successor execution environment supports pinned HElib, execute it.

If it does not support HElib/native execution:

do not count infrastructure probing as a substantive scientific turn;
do not redo source microaudits already closed;
choose the next highest-EIG independent paper-level correctness task that can change construction/correctness;
preserve the native blocker explicitly.

After recovery-canary PASS, exact parameter/interface verification must test:

SlotsToCtxts scalar Z5 outputs;
common ptxtSpace5/common f_in;
tagged forward at ptxtSpace5 against FullForward5;
five helper-A branch paths;
separate-vs-shared reconstruction equality;
ptxtSpace625 / factor1 / key0 reconstruction state;
mod5-to-Z625 lift bridge;
real normal_basis=false inverse;
factor1 -> scalar28 -> factor67;
exact 17-call recovery/routing;
independent per-slot residue/rho correction;
exact L0,L1,L2,L3;
all six Algorithm4 divide boundaries;
gcd(intFactor,5)==1 throughout Algorithm4;
final Recode at ptxtSpace5 using existing 625-typed keys;
only afterward restore f_in;
final decrypt equals source plaintext.

No timing before all correctness assertions pass.

Complete PAPER_CANDIDATE synchronized state
JSON
{
  "CANDIDATE_ID": "legacy-484479fe4613",
  "RANK": 1,
  "STATUS": "ACTIVE",
  "PHASE": "CORRECTNESS_GATE",
  "PAPER_THESIS": "Hypothesis under validation: reduce Aung et al.'s repeated MultKey bottleneck by starting from source-guaranteed scalar Z5 SlotsToCtxts branches, applying five globally tagged branch-local ThinEvalMap forwards exact modulo5, independently crossing the nonlinear recryption preprocessing boundary, aggregating only exact post-divide pairs, performing one ciphertext-state-exact recryptEkey reconstruction into an arbitrary Z625 lift, applying one stock-resource normal_basis=false Z625 inverse and scalar-unit normalization to factor67, recovering five branch-aligned arbitrary Z625 lifts with correct source residues, independently correcting/routing each physical SIMD slot, forming exact slotwise L0,L1,L2,L3, executing Algorithm4, final mod5 Recode, and only then restoring the saved application factor.",
  "IMPORTANT_PROBLEM": "Inherited important problem remains Aung et al.'s repeated per-branch MultKey cost in canonical p=5,m=32768,w=512,k=5 Corr./TnM. Turn25 does not reassess problem importance.",
  "BASELINE": "Primary baseline remains source-faithful Aung Corr./TnM at p=5,m=32768,w=512,k=5; secondary frontier remains matched vanilla HElib thin bootstrapping. The current candidate is statically typed end-to-end against the source semantics, but matched native baseline correctness is still pending.",
  "CLOSEST_PRIOR_ART": "The construction remains directly adjacent to Aung's correction-style RMFE bootstrapping and pinned HElib thin recryption. Turn25 adds no novelty claim; it closes the current static dependency graph and proves that independent arbitrary Z625 lifts across the two physical SIMD slots are sufficient because Aung Algorithm4 is slot-local and accepts arbitrary Z_{p^e} coefficients. NOVELTY_STATUS remains PREFLIGHT.",
  "NEW_MECHANISM": "Hypothesis under validation: five source scalar/common-factor branches are globally tagged and forwarded separately over Z5, each executes source-identical nonlinear preprocessing through exact /5, their two post-divide ZZX components are summed exactly, one stored recryptEkey reconstructs the aggregate at ptxtSpace625, a pure Z625 inverse and scalar-unit28 normalization feed the 17-call full-domain recovery, per-slot routing and public443 residue correction yield independently valid arbitrary Z625 branch lifts, four exact correction outputs are formed per slot, and Algorithm4 plus final Recode/f_in restoration completes bootstrapping.",
  "CONTRIBUTION_TYPE": "ALGORITHM",
  "FULL_CONSTRUCTION": "Fixed parameters are p=5,m=32768,w=512,k=5,r=1,e=4,e'=1,q=626, temporary ptxtSpace625, local degree8192, eta125, J=[0,1024,7168,2048,6144], branch labels [2,0,3,1,4]. Five SlotsToCtxts outputs have scalar Z5 physical slots and common f_in. Each branch receives a global monomial tag, stock pre-forward level preparation, tagged ThinEvalMap forward over Z5, then branch-local canonicalization/modDown/reLinearize/rawModSwitch/newMakeDivisible/exact divide-by5. The five exact ZZX pairs are summed and reconstructed once with recryptEkey at factor1. A normal_basis=false Z625 inverse whose reduction equals the mod5 inverse is followed by scalar-unit28 normalization to factor67 and the 17-call full-domain target-pruned recovery. Each physical slot independently yields arbitrary Z625 lifts of its source residues; known rho permutation and public443 correct the second-slot residue ordering/unit without requiring higher-adic cross-slot coherence. Exact local L0..L3 feed Algorithm4; its six divideByP boundaries preserve 5-adic unit factors; final Recode occurs at ptxtSpace5; f_in is restored afterward.",
  "CORRECTNESS": "Turn25 completes the current static typed dependency audit. Aung SIMD semantics are component-wise and Algorithm4 quantifies over arbitrary coefficients a_i in Z_{p^e}; therefore the two physical SIMD slots may independently use different arbitrary Z625 lift vectors. For nonzero second-slot target coordinates, recovered values need only have residue 2*b modulo5; multiplying by public443, whose residue is3, produces an arbitrary lift with residue b. Thus the existing routing/correction constants remain correct without assuming an exact lifted rho/182 relation. Each slot then forms exact L0..L3 from one internally consistent arbitrary lift vector and independently satisfies Algorithm4. Combined with Turns16-24 and the historical full-domain recovery/four-output theorems, no unidentified static semantic edge remains in the fixed construction. This is conditional static closure, not native candidate correctness.",
  "SECURITY": "PENDING. The static closure introduces no new key, secret exposure, or cryptographic assumption. Complete security and evaluation-key/resource audit remains required before a paper-level security gate can pass.",
  "NOISE_PRECISION_DFR": "PENDING. Branch-local source checks, exact shared-reconstruction norm envelope, factor-unit closure and structural recovery bounds are known, but actual native noiseBound/capacity trajectory, floating estimator behavior, Algorithm4 harmonization cost, DFR and final precision/correctness margins remain unverified.",
  "VALUE": "PENDING. Structural operation/key-reuse facts exist, including current transform-side count23 rather than stale19, but no performance verdict is authorized before baseline and complete candidate correctness under matched native conditions.",
  "CRITICAL_BLOCKER": "The mandatory evidence order remains blocked at the revised recovery-only native canary. Static semantic correctness for the fixed candidate is now closed conditionally, but no recovery canary, exact parameter/interface execution, matched baseline correctness or complete candidate native correctness has been obtained.",
  "NEXT_DECISIVE_TEST": "In the successor session execute the frozen revised recovery-only canary against homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON. After PASS, run the current exact interface oracle: assert SlotsToCtxts scalar/common-factor state; tagged forward at ptxtSpace5 against FullForward5; five helper-A paths; shared-vs-separate reconstruction ciphertext/metadata equality; reconstruction mod5-to-Z625 lift consistency; real normal_basis=false inverse; factor1 then scalar28 to factor67; exact 17-call routing/recovery; independent per-slot residue/rho correction and exact L0..L3; six Algorithm4 divide boundaries with unit-factor instrumentation; final Recode at ptxtSpace5; and final f_in restoration. Do not benchmark before these correctness checks pass.",
  "NOVELTY_STATUS": "PREFLIGHT",
  "PAPER_READINESS": "NOT_READY",
  "REOPEN_CONDITION": "Reopen the static theorem only if native execution falsifies one of the frozen interfaces, if an authenticated Aung artifact differs materially from the audited source contracts, if second-slot routing fails residue correction despite the current rho map, or if Algorithm4/native implementation requires cross-slot higher-adic lift coherence not present in the source theorem. Do not reopen merely because the two slots choose different arbitrary Z625 representatives.",
  "CONSTRUCTIVE_DESIGN_SPEC": "The construction explicitly separates application-mod5 and temporary-mod625 domains, preserves five branches through every nonlinear preprocessing step, aggregates only exact post-divide integer pairs, reconstructs once, uses the stock-resource power-basis inverse, unit-scalar normalization and full-domain pruned recovery, permits independent arbitrary Z625 lift vectors in the two SIMD slots, corrects only the required mod5 rho residue/permutation before exact four-output RMFE recombination, and keeps Algorithm4/final-Recode/intFactor restoration in their source-valid order. Stale one-forward, exact-lifted-rho, factor1 and transform-count19 descriptions are forbidden.",
  "CORRECTNESS_GATE": "BLOCKED",
  "SECURITY_GATE": "PENDING",
  "VALUE_GATE": "PENDING",
  "AUDIT_GATE": "PENDING",
  "BASELINE_CORRECTNESS": "PENDING",
  "GATE_JUSTIFICATIONS": {
    "CORRECTNESS_GATE": "The fixed candidate now has no identified static semantic/type gap, but mandatory native canary, exact interface execution, complete baseline correctness and full candidate correctness remain absent; static closure cannot substitute for those prerequisites.",
    "SECURITY_GATE": "No new security assumption is introduced by the static closure, but a complete security/resource audit has not been performed.",
    "VALUE_GATE": "Current structural counts and static bounds are not matched benchmark evidence; performance remains blocked on correctness.",
    "AUDIT_GATE": "The current work is an internal dependency audit, not the required independent raw paper-level audit.",
    "BASELINE_CORRECTNESS": "Source semantics are audited, but the matched source-faithful Aung baseline has not been executed and verified end-to-end."
  },
  "ASSESSMENT": {
    "MECHANISM_PROGRESS": false,
    "THEOREM_PROGRESS": true,
    "CORRECTNESS_PROGRESS": true,
    "SECURITY_PROGRESS": false,
    "VALUE_PROGRESS": false,
    "NOVELTY_PROGRESS": false,
    "REDUCES_CRITICAL_UNCERTAINTY": true,
    "EVIDENCE_GRADE": "MATH",
    "BASELINE_MATCHED": false,
    "PERFORMANCE_CLAIM": false,
    "OBSTRUCTION_VALUABLE": false,
    "STRICT_NO_GO": false,
    "CREDIBLE_NEW_MECHANISM": true,
    "FRONTIER_CANDIDATES_REMAINING": true,
    "INDEPENDENT_AUDIT_PASSED": false,
    "VALUE_REVIEW_COMPLETED": false,
    "VERDICT": "PASS"
  }
}

Durable extra state:

纯文本
CONSECUTIVE_LOW_VALUE_TURNS = 0
VALUE_REVIEW_STATE = NONE
VALUE_REVIEW_DUE_TURN = null
RESEARCH_POLICY_VERSION = paper-first-runtime-v2
PENDING_PI_DECISIONS = none
BACKUP_CANDIDATES = none
PI / autonomous research rules
Human PI is final authority on strategic research direction and scientific value.
Agent should autonomously continue reversible, low-regret, in-scope work.
Candidate/family failure => PARK/KILL and autonomously reprioritize within the same top-level objective.
Do not WAIT_PI merely because one candidate fails.
WAIT_PI only if the top-level frontier is genuinely exhausted.
Record reversible strategic choices as AI_PROVISIONAL_CHOICE if needed.
PENDING_PI_DECISION alone does not block independent work.
Never claim PI approval for a choice the PI did not make.
Codex / native delegation rules

Authorized cheapest-decisive native/Codex work does not require per-task PI approval.

Before native execution:

preserve exact task provenance;
avoid duplicate tasks;
do not rerun any task marked completed / do_not_rerun;
do not mutate another pending task's working directory/source/binary;
one heavy native task at a time unless explicitly justified.

When a task is pending:

result remains UNKNOWN;
do not reserve a research turn for it;
continue independent useful research if available;
the orchestrator will deliver the result to the latest active session.

When a result arrives:

independently audit it before accepting its conclusion;
preserve command/build/model/artifact provenance;
do not conflate task self-report with independently verified evidence.
Normal substantive-answer protocol

For every substantive research turn:

Keep the same TRACK_ID / ACTIVE_SUBLINE unless explicitly changed by PI.
Advance exactly one primary hypothesis.
Use one cheapest decisive test.
State a falsifier before serious work.
Avoid duplicate source microaudits already durably closed.
Maintain the current PAPER_CANDIDATE state.
Persist durable scientific results read-before-write.
Verify persistence.
Keep the final chat report concise and decision-oriented.
End the substantive research body with exactly one strict JSON <PAPER_CANDIDATE_UPDATE> block when the orchestrator prompt requests it.
PASS_STATIC/PASS_MATH never imply native correctness or PAPER_READY.
Preserve UNKNOWN/PENDING where evidence is absent.
No performance claim before correctness prerequisites.
Strict ORCHESTRATOR_CONTROL protocol

For every normal answer in the successor conversation, unless the current orchestrator prompt explicitly says that it wants the substantive body only and that a separate control envelope will follow, end with exactly one valid control block:

纯文本
<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

Rules:

action: CONTINUE

Use when autonomous in-scope research remains available and no new native task is being launched by this answer.
Normally requires_pi: false.
independent_research_available: true.

action: EXECUTE

Use only when this answer actually establishes/authorizes a concrete native/Codex task to launch.
Include:
task_id: <exact established task identifier>
inside the block.
Never invent a task_id.
Do not include task_id unless that identifier was explicitly established in the substantive answer.
A pending task from an older session is NOT a reason to emit EXECUTE again.

action: WAIT_PI

Allowed only if further progress genuinely requires PI input AND no useful independent research remains.
Must include:
requires_pi: true
independent_research_available: false
research_frontier_exhausted: true
Never use merely because a PENDING_PI_DECISION exists.

action: STOP

Allowed only if the top-level research objective is exhausted/terminated.
Must include:
research_frontier_exhausted: true
Never use for ordinary candidate failure while another in-scope path exists.

Whenever requires_pi: true, independent_research_available MUST be present and accurate.

For WAIT_PI or STOP, research_frontier_exhausted: true MUST be present.

milestone: true only for a material durable scientific result/checkpoint, not ordinary bookkeeping.

If the orchestrator explicitly requests:

纯文本
This message requests only the substantive research body.
Do not include ORCHESTRATOR_CONTROL.

then do NOT include a control block in that answer. A later control-repair prompt will request it separately.

If a later prompt says:

纯文本
Control-block repair only.

do not redo research, do not add claims, and output only the required control block based on the immediately preceding substantive answer.

Successor first action

Recover durable context from GitHub Notes / verified Git authority.

Then, without redoing Turns1–25, choose the next cheapest decisive CORRECTNESS_GATE step.

Preferred next action:

纯文本
execute frozen revised recovery-only native canary

if pinned HElib/native environment is actually available.

If native execution is unavailable, preserve the blocker and select a genuinely new paper-level correctness task with high expected information gain. Do not spend substantive turns re-proving already frozen static interfaces.

The research frontier is NOT exhausted.

Independent research remains available.
