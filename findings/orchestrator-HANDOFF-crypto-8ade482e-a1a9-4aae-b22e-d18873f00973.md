# 密码学 25.0 handoff

Resume research — Session Handoff

You are the formal Research GPT continuing an existing BOOT research program. This is a session continuation, not a new project. Preserve all durable scientific state and evidence-order constraints below.

Identity / session state

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED: Research Turn 25/25 — Session Closure
NEXT_ITERATION: Resume from this handoff and choose the next cheapest decisive paper-level test, subject to the pending-native-task preemption rule below.
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE
CONTINUOUS_AUTONOMOUS_RESEARCH: ENABLED
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
research_frontier_exhausted: false

The previous session exhausted its 25 substantive-turn capacity. Turn 26 in that session was HANDOFF ONLY and must not contain new research. The successor conversation may resume substantive research under the same TRACK_ID / ACTIVE_SUBLINE.

Exact next conversation name assigned by the orchestrator:
密码学 25.0

Latest durable checkpoint / authority

The read-before-write Git checkpoint succeeded at:

09528294cf2028530845b2665df726c309f9fe7d

Latest substantive Turn-25 durable finding:

findings/boot-successor-turn25-session-closure-and-successor-handoff-2026-11-03.md

Turn-25 finding commit:
c92a72531bd1a9f9014cb463500cba7bd6d17530

Turn-25 finding blob:
b4dbdd5d78207ea1310582e6b2023c9d215272df

GitHub Notes remained degraded during the session. Verified local BBBINGW/memory Git state is durable authority when connector reads are unhealthy. Connector failure must never by itself stop research.

Session accomplishments — Turns 8–25

The successor must treat the following as the current latest versions, not as independent competing claims.

Turn 8 — merged Method-1 pre-raw gate

Durable:
findings/boot-successor-turn8-merged-preraw-rawmodswitch-capacity-gate-2026-11-03.md

commit:
f86bf67fd3c3c88d5ec06cdd402a046ade9666d9

Main result:
The five Aung Method-1 projection branches can be merged before rawModSwitch under a static sufficient source-aligned gate. The merged candidate adds log2(5)=2.321928... bits versus one branch. Source-aligned sufficient input-capacity thresholds were derived. Full Frobenius one-hop key availability was also source-audited.

Turn 9 — exact Method-1 canary oracle

Durable:
findings/boot-successor-turn9-small-canary-oracle-execution-contract-gate-2026-11-03.md

commit:
717bcb2e7d78ebb4ed2b5f43bca8d65b77190e11

Main result:
Closed exact Method-1 trace-dual formula and arbitrary-lift recovery oracle. Important correction: reconstruction high p-adic digits need not equal canonical input lifts; only low digits modulo p must match before exact common-lift recovery.

Turn 10 — native Step-2 execution contract

Durable:
findings/boot-successor-turn10-native-step2-small-canary-execution-contract-2026-11-03.md

commit:
a584bdfd74a5d18e2b1fba28e67b753d6ce50df7

Main result:
Authorized exact small native canary contract. R1 was later superseded before execution.

Turn 11 — raw-L1 semantic repair and R2 authorization

Durable:
findings/boot-successor-turn11-raw-l1-source-semantics-canary-contract-repair-2026-11-03.md

commit:
ab255eb50098e728cbec0f56d1e4c9633267aab8

Mandatory supersession:
Use the centered TOTAL raw decryption polynomial returned by SecKey::Decrypt(...,raw).

Do NOT subtract semantic plaintext.

Define:
E_raw_L1(c)=sum_j |raw_j|

and:
C_in_native=log2(Q0/E_raw_L1(input)).

Authorized task:
BOOT-T11-R8-SMALL-CANARY-20261103-R2

R1 is superseded and must never be executed or interpreted as a scientific result.

Turn 12 — runtime-profile reproducibility boundary

Durable:
findings/boot-successor-turn12-aung-runtime-profile-reproducibility-boundary-2026-11-03.md

commit:
93ce8c686c087042e090455fa206de1947cfff4c

Mandatory provenance model:

PAPER_EXPLICIT:
only fields actually published by Aung.

NATIVE_SERIALIZED:
exact realized HElib context/key/prime/compiler/runtime profile.

Do NOT silently identify HElib defaults with unpublished Aung settings.
Do NOT claim author-exact binary/runtime reproduction from the paper alone.

Turn 13 — complete four-output correction front end

Durable latest Turn-13 authority:
findings/boot-successor-turn13-four-output-correction-map-shared-frobenius-closure-2026-11-03.md
and companion shared-orbit closure finding.

Latest Turn-13 commit:
cac6229cc5d193b72bcc5714d7a97096fd4f74dc

Main result:
The post-RM10 recovered state can produce all four Aung correction inputs L0,L1,L2,L3 from ONE common arbitrary Z625 lift vector using one shared eight-Frobenius bank.

This supersedes any earlier G0-only Algorithm-4 front-end description.

Turn 14 — coefficient-L1 proof-architecture no-go

Durable:
findings/boot-successor-turn14-algorithm4-u0-three-Fe-certificate-capacity-no-go-2026-11-03.md

commit:
52ac37783eadf276a8a8883a0323cea55bf1572a

Main result:
For the R2 h=120 profile, the old deterministic coefficient-L1 plus generic rounding proof architecture cannot certify the full three-F4 u0 chain. This is a proof-method obstruction, not an actual ciphertext-correctness failure.

Do not spend future turns tuning the same prefix/residue/K-factor route.

Turn 15 — exact canonical runtime-certificate route

Durable:
findings/boot-successor-turn15-exact-canonical-runtime-certificate-route-2026-11-03.md

commit:
77c905389b3621847fea75f744ee736e388281dc

Main result:
Pinned HElib real modDownToSet uses actual realized canonical norms of rounding polynomials, not merely the heuristic uniform-independent estimate. Secret and key-switch error canonical bounds are rejection-enforced. This gives a source-compatible exact/sample-specific canonical correctness route past Turn-14's coefficient-L1 obstruction.

Static conservative sufficient threshold for the u0 three-F4 chain:
log2(Q0)>408.4311452520461

At minimum Q0 floor 399.5 bits, a reference actual canonical rounding contribution threshold is approximately:
67,143,366.1530421

These are correctness-screening conditions, not measured results.

Turn 16 — complete six-boundary Algorithm-4 oracle

Durable:
findings/boot-successor-turn16-complete-algorithm4-six-boundary-canonical-acceptance-oracle-2026-11-03.md

commit:
7e88e69d0282b991eb20a3258b45a81987ec7f64

Main result:
Frozen complete Algorithm-4 acceptance oracle for p=5,e=4.

Plaintext-space ladder:
625→125
625→125
125→25
625→125
125→25
25→5

Every arithmetic event must maintain an independently upward-certified canonical bound C and satisfy:
C<0.48Q

For m=32768:
polyNormBnd=1

Final Recode occurs at ptxtSpace5.

A realized trace that passes every semantic/certificate assertion is a valid complete Algorithm-4 correctness certificate for that serialized trace, but not yet a distributional DFR theorem.

Turn 17 — public guard + matched-baseline fallback

Durable:
findings/boot-successor-turn17-public-certificate-guard-baseline-fallback-dfr-reduction-2026-11-03.md

commit:
8347c308901668bd0bf1cc0310b83d52f83e8826

Main result:
Preserve the five post-Method-1 projection ciphertexts, run the fast candidate only on copies, and on public certificate failure discard fast descendants and execute the matched split baseline from preserved snapshots.

Production guard does not require secret-key decrypt.

DFR reduction:
Pr[F_guarded] <= Pr[F_baseline]

without an independence assumption.

Fallback probability becomes a VALUE metric, not a correctness requirement.

Turn 18 — bounded novelty/value preflight

Durable:
findings/boot-successor-turn18-bounded-novelty-value-preflight-sparse-r8-one-multkey-2026-11-03.md

commit:
a682237a745b93a38ab700a168657464c8e99407

Main result:
Broad novelty claims were narrowed.

NOT standalone novelty:

shared Frobenius bank;
subring packing;
generic merge-before-key-switch;
multi-output shared encrypted intermediate.

Surviving candidate-specific delta:
Aung Method-1 outputs
→ one carrier
→ ONE ordinary HElib MultKey/raw reconstruction
→ one common dirty p^e-lift vector
→ correction-map interface.

p=5 value screening:
published Aung p=5 Corr.(TnM):
11.33 s total
4.732 s MultKey stage
post capacity 101
throughput ratio vs thin 0.832

Idealized 5→1 MultKey ceiling:
~7.5444 s total
~1.50x max end-to-end speedup

Thin-throughput frontier:
T_fast < 9.4016*(C_fast/101) seconds

Turn 19 — fixed-ring module carrier theorem / p=3 prescout

Durable:
findings/boot-successor-turn19-fixed-ring-module-carrier-generalization-p3-value-prescout-2026-11-03.md

commit:
5e91f6d2b18b747cbeec78652f3573735f653931

Main result:
The p=5 carrier is one instance of a broader fixed-ring module construction.

For p=3,w=512,k=7:
same Phi32 carrier is algebraically sufficient;
same RM10 + seven nonidentity Frobenius images;
five correction outputs;
combined normalization scale remains 8192.

p=3 remains prescout only, not active/back-up native candidate.

Turn 20 — all correction-row feasibility

Durable:
findings/boot-successor-turn20-fixed-ring-carrier-feasibility-table-all-correction-rows-2026-11-03.md

commit:
26413d32b4463d050400d0f6789a352617107c11

Main result:
All 19 published non-DNE Aung correction/TnM rows satisfy the fixed-ring carrier feasibility criterion.

General criterion:
f_q=f_out
and
k<=d_q

where:
d_q=ord_{2^q}(p)
f_q=phi(2^q)/d_q

Minimum feasible q also minimizes structural recovery-automorphism count.

This is a design/generalization theorem, not standalone novelty and not native evidence.

Turn 21 — paper-level VALUE_REVIEW

Durable:
findings/boot-successor-turn21-paper-level-value-review-anchor-vs-family-2026-11-03.md

commit:
ae7a8199c159080948d2dedc0bc4ace22e8ffdfb

VALUE_REVIEW_COMPLETED: true

Decision:
Do NOT park p=5 now.
Do NOT pivot now.

p=5 remains the cheapest correctness/reference anchor.

Future matched-value zones:

Zone A — FRONTIER_CROSSING:
T_fast < 9.4016*(C_fast/101)
→ p=5 itself can be empirical value anchor.

Zone B — DIRECT_BASELINE_WIN_ONLY:
beats Aung p=5 but not thin throughput
→ keep p=5 as correctness anchor;
at least one higher-k family row later required for stronger paper value.

Zone C — NO_DIRECT_VALUE:
p=5 Pareto-dominated by matched Aung baseline with no compensating resource/capacity gain
→ after evidence archival, PARK p=5 implementation anchor and provisionally promote p=3,w=512,k=7.

Turn 22 — independent-style prior-art stress test

Durable:
findings/boot-successor-turn22-independent-style-fixed-ring-prior-art-stress-test-2026-11-03.md

commit:
161f5ce54efaec5df8b45b5d2adc65f1b64a9ea3

Main result:
Broad fixed-ring/module theorem itself is prior art / standard algebra.

Do NOT claim standalone novelty for:

module-over-subring representation;
trace-dual coordinate recovery;
one key switch then multiple trace outputs;
shared Frobenius bank;
generic subring coefficient carrier.

Surviving narrow novelty:
known algebraic machinery placed ACROSS Aung/HElib stock MultKey/raw reconstruction so all components jointly undergo one nonlinear integer reconstruction and one same-lift p^e correction interface is recovered afterward.

Important novelty source gate:
ePrint 2026/927,
"Fully Homomorphic Encryption on the Ring of Gaussian Periods",
full text still requires independent exact-collision audit before NOVELTY_STATUS may become CLEAR.

Turn 23 — security / key-footprint pre-audit

Durable:
findings/boot-successor-turn23-security-key-footprint-preaudit-2026-11-03.md

commit:
6a3fda613a6cb3d7d537afad14a1776187bdc4f8

Main result:
No new secret/ring assumption family.

Same secret-key IDs:
{key0,key1}

Same recryptEkey / recryption cycle.

All candidate direct automorphisms lie in the p=5 Frobenius subgroup.

Direct candidate Frobenius exponent set has 23 unique targets:
{1,2,3,4,5,6,7,8,16,32,64,128,256,888,2032,3968,4096,5088,6080,6144,7168,7680,7936}

Under standard pinned HElib addFrbMatrices, all 8191 nonidentity Frobenius matrices already exist.

Therefore under COMMON-STANDARD profile:
incremental candidate Frobenius matrices = 0
guarded union keyset collapses to baseline keyset.

But:
MINIMIZED-PER-WORKFLOW key delta remains UNKNOWN.
Do not convert standard-profile zero delta into a minimized-key-size claim.

Concrete multi-sample security remains pending.

Turn 24 — pre-Step3 readiness / baseline-interface audit

Durable:
findings/boot-successor-turn24-prestep3-readiness-and-baseline-interface-audit-2026-11-03.md

commit:
f339f49c49d45dd274d252a13daec67352248b1b

Main result:
No new unidentified static fast-path semantic blocker.

Therefore:
R2 scientific PASS
→ open Step 3 only.

Matched baseline claim refined to:
MATCHED_SOURCE_FAITHFUL_REFERENCE_PROFILE

not:
AUTHOR_EXACT_REPRODUCTION.

Reason:
Aung Algorithm 2 is conceptual and does not uniquely determine exact pinned-HLib native operation ordering/runtime profile.

Step-4 baseline uses same five Method-1 outputs and the same serialized Tier-B runtime profile, then each split branch follows the pinned thinReCrypt pre-digit-extraction source shape through coeffToSlot, followed by Aung correction maps / Algorithm4 / final Recode.

Published Aung timings/capacities are fingerprints, not exact acceptance values.

Turn 25 — session closure

Durable:
findings/boot-successor-turn25-session-closure-and-successor-handoff-2026-11-03.md

commit:
c92a72531bd1a9f9014cb463500cba7bd6d17530

blob:
b4dbdd5d78207ea1310582e6b2023c9d215272df

Final verdict:
PASS_SESSION_CLOSURE_CONSISTENCY_AUDIT
PASS_SUCCESSOR_HANDOFF_STATE_FROZEN
PASS_NO_NEW_IDENTIFIED_STATIC_SEMANTIC_BLOCKER
PASS_EVIDENCE_ORDER_FROZEN
PASS_STEP3_STEP4_STEP5_CONTRACTS_FROZEN
PASS_VALUE_POLICY_FROZEN
PASS_NOVELTY_CLAIM_BOUNDARY_FROZEN

No new R2 result existed in durable repo at Turn 25.

Current strongest candidate

CANDIDATE_ID:
rmfe-subring-envelope-single-multkey-v1

Rank:
1

Status:
ACTIVE

Contribution type:
ALGORITHM

Phase:
CORRECTNESS_GATE

Active native target only:
p=5
m=32768
w=512
k=5
Aung Corr.(TnM)

Higher-k p=3,p=7,... rows are prescout/generalization only.
No ranked BACKUP candidate is currently active.

Current main hypothesis

Known subring/trace/Frobenius machinery can be placed across Aung's previously open direct-RMFE-MultKey interface so that the five Method-1 RMFE components remain jointly represented through one ordinary HElib MultKey/raw reconstruction in the same outer BGV ring, after which one common arbitrary-Z625 dirty-lift vector is recovered and used to construct all four correction-map inputs.

The novelty claim is NOT the fixed-ring/module/trace algebra itself.

The surviving candidate-specific mechanism is:

encode Method-1 outputs before the recryption-key inner product;
perform one common reLinearize/rawModSwitch/newMakeDivisible/recryptEkey reconstruction;
delay coordinate recovery until after that integer-rounding path;
accept arbitrary high p-adic digits;
derive all correction maps from the exact same common dirty-lift state.
Current PAPER_CANDIDATE — synchronized durable state

{
"candidate_id": "rmfe-subring-envelope-single-multkey-v1",
"rank": 1,
"status": "ACTIVE",
"phase": "CORRECTNESS_GATE",
"paper_thesis": "Hypothesis: known subring/trace/Frobenius machinery can be placed across Aung's previously open direct-RMFE-MultKey interface so that Method-1 RMFE components remain jointly represented through one ordinary HElib bootstrapping-key MultKey/raw reconstruction in the same outer BGV ring, after which one common arbitrary-p-adic dirty-lift vector is recovered and used to construct all correction-map inputs. The active p=5,w=512 instance remains the first native target of a broader parameter family.",
"important_problem": "Aung explicitly leaves direct MultKey on RMFE-packed ciphertext as future work. The active p=5,w=512 row spends 4.732 seconds of 11.33 seconds in repeated split MultKey work, while higher-k rows offer a broader value family if the interface mechanism survives native evidence.",
"baseline": "Matched baseline is frozen as a source-faithful reference-profile Aung p=5,w=512,k=5 Corr.(TnM) implementation rather than an author-exact binary reproduction. It begins from the same five Method-1 outputs, uses the same serialized Tier-B HElib profile, runs the pinned thinReCrypt pre-digit-extraction branch shape separately through coeffToSlot, then performs Aung CtxtsToSlots/correction maps, Algorithm4 and final Recode. Published capacities/timings remain fingerprints.",
"closest_prior_art": "Gentry-Halevi-Peikert-Smart field switching provides module-over-subring representations, trace-linear recovery and multiple outputs after one key switch; Alperin-Sheriff-Peikert and Geelen-Vercauteren provide bootstrapping subring/coefficient-selection machinery; FIMD provides RMFE Frobenius maps and shared automorphism banks. None of the inspected sources performs Aung's ordinary BGV MultKey/raw reconstruction once on an RMFE component carrier and then recovers same post-reconstruction p-adic lifts for correction DigitExtract. ePrint 2026/927 remains the highest-priority source-gated close prior.",
"new_mechanism": "Method-1 outputs are encoded as carrier coefficients before the recryption-key inner product; one common reLinearize/rawModSwitch/newMakeDivisible/recryptEkey reconstruction is executed in the original outer ring; coordinate recovery is delayed until afterward; arbitrary high p-adic digits are retained as one common dirty lift vector; and all Aung correction maps are derived from that vector. No subring secret, new ring, new recryption-key cycle or new assumption family is introduced.",
"contribution_type": "ALGORITHM",
"full_construction": "Five p=5 Method-1 projections -> fixed-ring/sparse Phi32 carrier -> one stock coefficient-domain HElib MultKey/reconstruction -> RM10 -> shared eight-Frobenius recovery -> exact common-lift L0-L3 -> scalar-unit28/intFactor67 -> Aung Algorithm4 with six certified divide boundaries -> final ptxtSpace5 Recode -> final application-factor restoration. Optional guarded execution retains immutable post-projection snapshots and falls back to the matched split baseline.",
"correctness": "Turn25 freezes the end-to-end static state: no unidentified fast-path semantic edge remains among Method1 scalar typing, carrier injection, merged raw gate, dirty-lift reconstruction, RM10, same-lift L0-L3, normalization, Algorithm4 event semantics, final Recode and key interface. Candidate correctness is not PASS because Native Step2 R2 and subsequent Steps3-5 remain unexecuted. R2 scientific PASS opens Step3 only.",
"security": "Assumption-family pre-audit passes: no new secret/ring assumption, recryption cycle or subring secret is introduced. Under the standard full-Frobenius HElib profile, candidate incremental Frobenius key material is zero. Minimized per-workflow key delta, public RLWE sample counts and exact concrete-security bits remain pending Step3/6.",
"noise_precision_dfr": "Exact-canonical realized-trace certification and optional guarded fallback remain the planned correctness/DFR routes. Complete native Algorithm4 certification and concrete DFR remain pending. No noise result is transferred to generalization rows.",
"value": "VALUE_REVIEW is complete. Zone A crosses thin throughput and allows p=5 to be the empirical anchor; Zone B beats the direct Aung baseline but requires a later higher-k family row for stronger paper value; Zone C fails direct value and triggers eventual parking/pivot after evidence archival. No matched benchmark has executed.",
"critical_blocker": "BOOT-T11-R8-SMALL-CANARY-20261103-R2 remains pending and must be independently audited. No additional static theorem blocker is identified. If R2 passes, Step3 exact parameter/interface serialization is the next legal evidence step.",
"next_decisive_test": "If BOOT-T11-R8-SMALL-CANARY-20261103-R2 becomes available, the next substantive turn must independently audit its raw artifacts without rerunning it. PASS opens Step3 only; scientific FAIL reopens the first failing stage; INFRA_BLOCKED leaves Step2 pending. If R2 remains pending, continue with the cheapest independent paper-level uncertainty rather than duplicating native work. Highest-priority novelty uncertainty is full-text exact-collision audit of ePrint 2026/927.",
"novelty_status": "PREFLIGHT",
"paper_readiness": "NOT_READY",
"reopen_condition": "Reopen the frozen static construction only if R2 or later native evidence falsifies one of the explicit interfaces. Mark NOVELTY_STATUS=COLLISION if verified prior art, including 2026/927, already carries multiple RMFE components through one ordinary BGV/BFV bootstrapping-key reconstruction and recovers all component p-adic lifts from the same post-reconstruction state for RMFE digit extraction. Generalization rows remain prescout-only until p=5 evidence/value justifies escalation.",
"constructive_design_spec": "Active p=5 design and native acceptance contracts are frozen. Raw-L1 uses the TOTAL centered raw decryption polynomial; runtime provenance is two-tier PAPER_EXPLICIT/NATIVE_SERIALIZED; full candidate correctness requires G0-G3 from one reconstruction oracle, the complete six-boundary Turn16 Algorithm4 event stream, final ptxtSpace5 Recode and factor restoration. Step4 uses a matched source-faithful reference baseline, not an author-exact reproduction. Standard-profile key reuse must not be confused with minimized-key equivalence.",
"correctness_gate": "BLOCKED",
"security_gate": "PENDING",
"value_gate": "PENDING",
"audit_gate": "PENDING",
"baseline_correctness": "PENDING",
"gate_justifications": {
"CORRECTNESS_GATE": "No static semantic edge remains identified, but mandatory Native Step2 is pending and Steps3-5 remain unexecuted.",
"SECURITY_GATE": "Assumption-family pre-audit passes, but exact serialized key/sample inventory, concrete security and DFR remain pending.",
"VALUE_GATE": "VALUE_REVIEW and objective benchmark zones are frozen, but matched correctness/security/performance evidence is absent.",
"AUDIT_GATE": "No independent raw implementation audit or complete independent prior-art audit has passed; 2026/927 full text remains a novelty source gate.",
"BASELINE_CORRECTNESS": "The matched source-faithful baseline contract is frozen but has not been executed or independently verified; author-exact binary reproduction is not supported by the publication alone."
},
"consecutive_low_value_turns": 0,
"value_review_state": "NONE",
"value_review_due_turn": null,
"research_policy_version": "paper-first-runtime-v2",
"policy_adopted_at": "2026-11-03T04:51:22.114Z",
"policy_provenance": "runtime shell initialization; scientific fields remain UNKNOWN"
}

Gate state

CORRECTNESS_GATE:
BLOCKED

Reason:
Native evidence Step 2 remains pending; Steps 3-5 unexecuted.

BASELINE_CORRECTNESS:
PENDING

SECURITY_GATE:
PENDING

VALUE_GATE:
PENDING

AUDIT_GATE:
PENDING

NOVELTY_STATUS:
PREFLIGHT

PAPER_READINESS:
NOT_READY

VALUE_REVIEW_COMPLETED:
true

INDEPENDENT_AUDIT_PASSED:
false

Evidence order — mandatory

Do not skip or infer prerequisites.

Source audit
Small correctness canary
Exact parameter/interface verification
Complete baseline correctness
Complete candidate correctness
Noise/security/DFR compatibility
Matched benchmark/value
Independent raw audit

Current state:
Step 1: PASS
Step 2: PENDING R2
Step 3+: BLOCKED by prior steps

Step-3 frozen contract

If and only if R2 receives an independently audited scientific PASS, Step 3 opens.

PAPER_EXPLICIT must include only published/source-explicit fields such as:

HElib commit acdb264e1a991eaee35fd8b3c31bebe9528c49a1
m=32768
p=5
application r=1
bits=400
w=512
k=5
Corr.(TnM)
observable paper e=4
single-thread where source-explicit

NATIVE_SERIALIZED must record exact realized:

c / nDigits
effective skHwt
scale / stdev / resolution
bitsInSpecialPrimes input
exact prime sets/products
digit partition
rcData.e / rcData.ePrime
mvec/gens/ords
build flags
NTL/GMP/platform
exact KeySwitch inventory
matrix plaintext spaces
direct-reachability strategy
serialized key bytes/sample counts

Aung published bit-width/capacity/timing values are fingerprints, not author-exact acceptance criteria.

Step-4 frozen baseline contract

Label:
MATCHED_SOURCE_FAITHFUL_REFERENCE_PROFILE

Not:
AUTHOR_EXACT_REPRODUCTION

Baseline begins from same five Method-1 outputs as candidate.

Each split branch uses same serialized Step-3 profile and pinned HElib thinReCrypt PRE-DIGIT-EXTRACTION source shape through coeffToSlot.

Then execute:
Aung CtxtsToSlots/correction-map construction
→ Algorithm4
→ final Recode

Do not call stock extractDigitsThin in the matched Aung correction baseline.

Published Aung Table-2 values remain fingerprints only.

Step-5 frozen candidate-completeness contract

Must include:

exact Step-3 serialized profile
core R2 chain
G1,G2,G3 in addition to G0
all four maps checked against ONE common reconstruction-coordinate oracle
complete Turn-16 Algorithm4 ordered event stream
six divide-boundary semantic assertions
canonical C<0.48Q checks at every reducing event
ptxtSpace/intFactor/primeSet transitions
final Recode oracle at ptxtSpace5
final application-factor restoration

If guarded mode:
force fallback at:

before sparse merge
after one MultKey
inside first F4
immediately before B6

and verify snapshot immutability plus matched-baseline output equivalence.

Mandatory supersession rules

Raw-L1:
Use TOTAL centered raw decryption polynomial.
Never subtract plaintext.

R2:
R1 is superseded before execution.
Never execute or infer R1.

Runtime provenance:
Use PAPER_EXPLICIT + NATIVE_SERIALIZED.
Never claim unpublished Aung runtime details as facts.

Novelty:
Do not claim fixed-ring/module/trace/Frobenius/shared-bank/generic merge-before-key-switch as standalone novelty.

Key footprint:
Standard-profile zero incremental Frobenius keys does not imply minimized-key equality.

Baseline:
Call it matched source-faithful reference profile unless author code/runtime artifacts are recovered.

Killed / superseded routes

Superseded native canary R1:
DO NOT EXECUTE.

Generic coefficient-L1 repeated-F4 proof architecture:
FAIL for h=120 under Turn-14 assumptions.
Do not return to prefix/residue/K-factor micro-tuning.

Standalone novelty claims for:
fixed-ring module theorem
trace-dual coordinate recovery
shared Frobenius bank
generic subring packing
generic merge-before-key-switch
one-key-switch/multi-trace-output
are all rejected by prior art.

Author-exact baseline reproduction from publication alone:
REJECTED.

p=3 / p=7 native generalization:
NOT AUTHORIZED YET.
Prescout only.

Strongest remaining novelty uncertainty

Highest-priority independent paper-level uncertainty outside the pending native evidence order:

Full-text exact-collision audit of:

ePrint 2026/927
"Fully Homomorphic Encryption on the Ring of Gaussian Periods"

Exact collision criterion:
Mark COLLISION if prior work already:

starts from multiple RMFE/FIMD/component plaintext values in one BGV/BFV context;
encodes them into one carrier before the ordinary bootstrapping-key/recryption inner product;
executes that expensive MultKey/recryption reconstruction only once;
after integer/raw reconstruction recovers all p-adic component lifts from the same post-reconstruction state;
feeds those common lifts into RMFE bootstrapping/digit extraction.

Generic subring/trace/field-switching prior art alone is insufficient for exact collision.

Value policy

Future p=5 matched benchmark zones:

Zone A:
T_fast < 9.4016*(C_fast/101)
→ crosses thin throughput; p=5 can be final empirical anchor.

Zone B:
beats direct Aung p=5 but not thin
→ p=5 remains correctness anchor;
later higher-k family benchmark required for stronger paper value.

Zone C:
no direct Pareto value
→ after evidence archival PARK p=5 implementation anchor and provisionally promote p=3,w=512,k=7.

No pivot is active now.

Generalization state

All 19 published non-DNE Aung correction rows are algebraically carrier-feasible.

No generalization row is ACTIVE or BACKUP.

Prescout preference if p=5 later justifies escalation:

p=3,w=512,k=7 — lowest-risk replication
p=3,w=1024,k=13 — higher leverage
p=7,w=1024,k=21 — strongest structural leverage / four physical factors

Do not spend native resources on these before p=5 evidence/value justifies it.

Research philosophy

Use the durable paper-first philosophy:

smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted

Every substantive turn must have:

one primary hypothesis
one minimal decisive test
an explicit failure condition
a paper-level uncertainty it reduces

Do not accumulate local PASS/FAIL facts that cannot change:

thesis
construction
correctness
security
value
novelty
audit verdict

Default philosophy:
先证明有洞，再想怎么填；先 falsify，再 optimize。

Do not treat "nobody seems to have done X" as sufficient novelty.

Prefer:
existing mechanism
→ exact obstruction/gap
→ minimal nontrivial representation/proof/interface fix
→ correctness/security/value/audit

PI / autonomy rules

PENDING_PI_DECISIONS:
none

PENDING_PI_DECISION is advisory, not automatically blocking.

If future PI decisions exist:

pending PI decision + independent work available => continue reversible low-regret work
pending PI decision + no independent work available => WAIT_PI

Never WAIT_PI merely because a decision is inherited.

CONTINUOUS_AUTONOMOUS_RESEARCH remains enabled.

NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION:
false

Authorized cheapest-decisive Codex/native execution does not require per-task PI authorization.

Candidate/family failure:

park or kill it;
autonomously reprioritize within the same top-level objective;
do not WAIT_PI while an ACTIVE or ranked BACKUP candidate has a credible decisive test.

WAIT_PI or STOP is legal only if the top-level research frontier is exhausted and the control block explicitly contains:
research_frontier_exhausted: true

Current:
research_frontier_exhausted: false

Pending Codex/native task provenance — background only

The following task is already running in the background.

It must NOT be restarted, duplicated, modified, resubmitted, or treated as complete.

task_id:
BOOT-T11-R8-SMALL-CANARY-20261103-R2

origin_session_id:
8ade482e-a1a9-4aae-b22e-d18873f00973

origin_session:
密码学 24.0

origin_turn:
11

original_hypothesis:
TASK_ID: BOOT-T11-R8-SMALL-CANARY-20261103-R2
Research Turn 11/25 — CORRECTNESS_GATE

The task tests the repaired Native Step-2 sparse-R8 small canary using Turn-10's full execution contract plus Turn-11's raw-L1 semantic repair. It must use TOTAL centered raw-decryption coefficient-L1, not plaintext-subtracted error. It must validate the exact Method-1 projection, sparse carrier, source-aligned pre-raw gate, rawModSwitch behavior, common dirty reconstruction, RM10, fused recovery, scalar normalization and exact Z625 oracle, and must stop before Algorithm4/DigitExtract/benchmark.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
max

pid_or_remote_execution_identity:
13383

start_time:
2026-11-03T08:52:19.336Z

current_status:
RUNNING

expected_artifacts:
[]

artifact_count:
0

evidence_status:
PENDING

audit_status:
PENDING

result_delivered:
false

do_not_rerun:
true

commit:
null

durable_evidence_reference:
orchestrator.db codex_tasks.task_id=BOOT-T11-R8-SMALL-CANARY-20261103-R2

Cross-session task rule:
Pending task lifecycle is independent of this Research GPT session.
Do not wait for it before performing independent no-regret research.
Do not reserve a local audit turn for it.
When its result becomes ready, the orchestrator will deliver it to the latest active session and it PREEMPTS that session's next free substantive turn for independent audit.

If raw R2 result arrives:

do not rerun;
independently inspect all raw artifacts/provenance;
all scientific assertions PASS => PASS_SMALL_CORRECTNESS_CANARY and open Step 3 only;
first scientific assertion FAIL => FAIL_SMALL_CORRECTNESS_CANARY and reopen only first failing semantic/interface stage;
build/dependency/runner failure => INFRA_BLOCKED and Step 2 remains pending.
Current next cheapest decisive test

Priority rule:

If R2 raw result is delivered:
independently audit R2 immediately.

If R2 is still pending:
choose the cheapest independent paper-level uncertainty that materially changes the paper.
Highest-priority currently recorded independent uncertainty:
full-text exact-collision audit of ePrint 2026/927.

Do not:

rerun R2;
start p=3/p=7 native work;
benchmark before evidence order permits;
repeat coefficient-L1 prefix tuning;
repeat broad novelty search already closed by Turn 22;
repeat VALUE_REVIEW.
Required paper-update discipline

At the end of each normal substantive research answer, emit exactly one strict JSON:

<PAPER_CANDIDATE_UPDATE>
{"CANDIDATE_ID":"...","RANK":1,"STATUS":"ACTIVE|BACKUP|PARKED|KILLED|PAPER_READY","PHASE":"PROBLEM_SELECTION|NOVELTY_PREFLIGHT|CONSTRUCTIVE_DESIGN|CORRECTNESS_GATE|SECURITY_GATE|VALUE_GATE|PAPER_AUDIT","PAPER_THESIS":"...","IMPORTANT_PROBLEM":"...","BASELINE":"...","CLOSEST_PRIOR_ART":"...","NEW_MECHANISM":"... or NO_CREDIBLE_NEW_MECHANISM","CONTRIBUTION_TYPE":"ALGORITHM|SYSTEM|SECURITY|THEORY|UNKNOWN","FULL_CONSTRUCTION":"...","CORRECTNESS":"...","SECURITY":"...","NOISE_PRECISION_DFR":"... or NOT_APPLICABLE with reason","VALUE":"...","CRITICAL_BLOCKER":"...","NEXT_DECISIVE_TEST":"...","NOVELTY_STATUS":"UNKNOWN|PREFLIGHT|CLEAR|COLLISION","PAPER_READINESS":"UNKNOWN|NOT_READY|READY","REOPEN_CONDITION":"...","CONSTRUCTIVE_DESIGN_SPEC":"...","CORRECTNESS_GATE":"UNKNOWN|PENDING|PASS|FAIL|BLOCKED|NOT_APPLICABLE","SECURITY_GATE":"UNKNOWN|PENDING|PASS|FAIL|BLOCKED|NOT_APPLICABLE","VALUE_GATE":"UNKNOWN|PENDING|PASS|FAIL|BLOCKED|NOT_APPLICABLE","AUDIT_GATE":"UNKNOWN|PENDING|PASS|FAIL|BLOCKED|NOT_APPLICABLE","BASELINE_CORRECTNESS":"UNKNOWN|PENDING|PASS|FAIL|BLOCKED|NOT_APPLICABLE","GATE_JUSTIFICATIONS":{},"ASSESSMENT":{"MECHANISM_PROGRESS":false,"THEOREM_PROGRESS":false,"CORRECTNESS_PROGRESS":false,"SECURITY_PROGRESS":false,"VALUE_PROGRESS":false,"NOVELTY_PROGRESS":false,"REDUCES_CRITICAL_UNCERTAINTY":false,"EVIDENCE_GRADE":"NONE|TOY|STATIC|MATH|BASELINE|MATCHED_BENCHMARK|INDEPENDENT_AUDIT","BASELINE_MATCHED":false,"PERFORMANCE_CLAIM":false,"OBSTRUCTION_VALUABLE":false,"STRICT_NO_GO":false,"CREDIBLE_NEW_MECHANISM":false,"FRONTIER_CANDIDATES_REMAINING":false,"INDEPENDENT_AUDIT_PASSED":false,"VALUE_REVIEW_COMPLETED":false,"VERDICT":"PASS|FAIL|UNCLEAR|HUMAN_REVIEW"}}
</PAPER_CANDIDATE_UPDATE>

Preserve UNKNOWN where evidence is absent.

PASS_TOY / PASS_STATIC / PASS_MATH never imply PAPER_READY.

Performance verdict is blocked until baseline correctness and matched conditions are verified.

NOVELTY_STATUS=CLEAR only after independent prior-art audit.

Strict ORCHESTRATOR_CONTROL protocol for every normal answer

Every normal answer in the successor research conversation must end with exactly one separate control block after the substantive body and after PAPER_CANDIDATE_UPDATE:

<ORCHESTRATOR_CONTROL>
action: CONTINUE|EXECUTE|WAIT_PI|STOP
milestone: true|false
requires_pi: true|false
independent_research_available: true|false
task_id: <explicit task id only when action is EXECUTE and the exact task_id has already been established>
research_frontier_exhausted: true|false
</ORCHESTRATOR_CONTROL>

Rules:

CONTINUE
Use when:
research can proceed independently without launching a new native/Codex task;
a Codex/native slot is already occupied and side research continues;
no PI decision blocks all work.

For CONTINUE:

task_id must be omitted.
research_frontier_exhausted should normally be false.
requires_pi should normally be false unless a PI advisory exists but independent work remains.
if requires_pi=true, independent_research_available MUST be included and truthfully set.
EXECUTE
Use only when:
a specific cheapest-decisive native/Codex task should now be launched;
the exact task_id is explicitly established in the same research state.

For EXECUTE:

task_id is mandatory.
do not invent a task_id.
do not EXECUTE a task already pending/running/do_not_rerun.
requires_pi=false for already authorized cheapest-decisive execution under continuous autonomous research unless an explicit PI-only issue exists.
research_frontier_exhausted=false.
WAIT_PI
Use only when:
a genuine PI decision blocks all meaningful independent progress;
there is no reversible low-regret independent work;
no ACTIVE or ranked BACKUP candidate has a credible decisive test.

Mandatory:
requires_pi=true
independent_research_available=false
research_frontier_exhausted=true

WAIT_PI is invalid merely because:

a native task is pending;
a connector is unavailable;
one candidate fails while other in-scope options remain.
STOP
Use only when:
the top-level authorized research frontier is exhausted or the research objective is completed/terminated.

Mandatory:
research_frontier_exhausted=true

Do not STOP merely because:

current candidate is blocked;
one native task is pending;
more independent work exists.
milestone
Set true when the turn:
closes a theorem/interface gate;
kills/parks a meaningful route;
changes paper candidate status/phase;
freezes a durable execution contract;
completes a value/security/novelty audit;
establishes a durable handoff-worthy result.

Otherwise false.

requires_pi / independent_research_available
If requires_pi=true, independent_research_available MUST be present.
If requires_pi=false, still include independent_research_available for consistency.

task lifecycle
Never infer pending task success from action=EXECUTE or from elapsed time.
Never duplicate a do_not_rerun task.
When a pending result arrives, audit it rather than rerunning it.

HANDOFF-only exception
If explicitly instructed that the current answer is HANDOFF ONLY, obey the handoff format requested by the orchestrator instead of emitting ORCHESTRATOR_CONTROL.

Response style

Keep chat reports concise, complete and decision-oriented.

Persist:

derivations;
evidence matrices;
experiment tables;
exact source provenance;
scripts/hashes;
long audit notes

to durable Git findings.

Do not repeat durable context unnecessarily in chat.

Do not reveal or imply pending native results.

Do not claim connector-derived facts when the connector is unhealthy unless independently verified through exact Git/source authority.
