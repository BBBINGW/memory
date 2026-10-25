# EAI-SYNTH Independent Research State — modular checkpoint
Checkpoint: 2026-10-26 (Asia/Singapore)
Repository BBBINGW/memory
TRACK_ID: EAI
ACTIVE_TOPIC: SYNTHETIC_DATA
ACTIVE_SUBLINE: EAI-SYNTH
LATEST_COMPLETED: SYNTH-C10
NEXT_CANDIDATE: SYNTH-C11_NOT_STARTED
SESSION STATUS: STRATEGIC_REVIEW_RECOMMENDED; NO new research execution without PI next authorization.
PI has sole final say on directions, novel contribution, pivot, experiments and disclosure. Research agent implements one smallest falsifiable claim and one cheapest decisive test each authorized round. Never start Codex, models, GPU, remote environments, downloads, repositories outside EAI-SYNTH notes or another research line without separate permission. User explicitly instructed hold ANY Codex tasks pending WITHOUT presenting commands until request.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO; NO tasks executed, no Codex prompt sent. C10 requires no Codex.

## C10 just completed
H-C10: raw <g_R,g_s> sample utility ranking is preserved for actual one-step real loss improvement under non-scalar positive optimizer preconditioning. FALSE. Exact quadratic L_R(theta)=.5||theta||², theta=(1,1), D=diag(4,1), eta=.1, two synthetic gradients A=(0,2), B=(1,0): raw score A2>B1, yet optimizer-step target loss reduction A=.18<B=.32. D is a frozen local AdamW-like diagonal preconditioner, NOT exact full AdamW history nor native run.
STRONG direct prior: Wang et al OPUS ICML2026 official PMLR 306 https://proceedings.mlr.press/v306/wang26gc.html, author site https://yancyou.github.io/OPUS_page/, public original preprint text Eq19–21/Algorithm1; existing optimizer-induced update scoring with Ghost+CountSketch and Boltzmann diversity, author reports +4.7% compute. Final PMLR PDF served as octet-stream and could NOT be visually inspected; author original public preprint text and publisher abstract were read. FROST Sep2026 raw-gradient original Eq2–6 https://arxiv.org/html/2609.29988 does not claim all optimizer ranking equivalence.
Additional directly SYNTH prior: Kessler et al COLM2026 'Towards Active Synthetic Data Generation for Finetuning Language Models' arXiv2512.00884v2 https://arxiv.org/pdf/2512.00884 original FULL 37-page PDF read and physical pp4/p6 screenshots inspected. Algorithm1 iterates learner-guided high-loss/uncertainty selection and teacher generation with fixed teacher/sample budget; §5 four reasoning tasks/students. Already budgeted closed-loop synthetic generation; OPUS targets pretraining/continued pretraining, not same synthetic SFT. Neither an automatically successful naive composition nor published joint end-to-end proof derived.
STATUS: FAIL_C10_RAW_GRADIENT_ALIGNMENT_RANK_EQUIVALENCE_UNDER_PRECONDITIONER.
RESULT: STRICT exact rank reversal; DIRECT 2026 OPUS optimizer-aware mitigation with author-reported low overhead.
NOVELTY: FAIL for optimizer-aware update scoring/CountSketch/active budgeted synthetic generation. Global EAI-SYNTH novelty still NOT_ESTABLISHED.
FULL FINDINGS: findings/eai-synth-c10-optimizer-aware-synthetic-selection-priorart-gate-2026-10-26.md
NEGATIVE ARCHIVE: failures/eai-synth-c10-optimizer-oblivious-raw-gradient-rank-no-go-2026-10-26.md
STATE_UPDATE: YES, readback verified.

## Prior archived rounds / isolation
B01–B12: finite-domain DP/Wasserstein/He sparse counting and noise-lifetime semantic audits. B11/B12 sparse counting noise semantics PARK; not author-vulnerability confirmation.
C01–C05: rare prevalence, verifier, mixture identifiability and standard private moment tests; all FAIL novelty, PARK.
C06–C07: Wasserstein distance versus task risk, barycenter versus pooled covariance, direct known ICLR/ICML/Management Science prior art; PARK.
C08: labeled real training mini-batch gradients can replace extra verifier for local utility; FROST arXiv2609.29988 direct prior; FAIL.
C09: fixed finite dataset re-use does not automatically satisfy FROST Appendix Eq18 martingale-difference population gradient assumption; exact EMA MSE floor 1/n, source theorem VALID if assumptions hold; direct adaptive-data reuse prior; FAIL.
Detailed individual evidence lives in existing findings/eai-synth-*.md and failures/eai-synth-*.md; original giant root STATE.md preserves exact old checkpoints. DO NOT overwrite/rewrite it due to file size limit (~259k characters at C09).

## Strategic research interpretation / NEXT
C01–C10 source searches produced meaningful assumptions/interfaces but NONE a substantiated NEW ALGORITHM with proof + meaningful end-to-end throughput/quality budget frontier. Repeated near-neighbor toy counterexamples are now a poor use of resources. If PI says continue, ONE C11 strategic first-party SOURCE-FIRST opportunity/novelty gate, not automatically another optimizer-gradient toy. One candidate, only if an exact new TECHNICAL claim can be framed: analyze combined fixed-budget teacher-generation cost + optimizer-aware training selection and its complete quality-cost interface, check Kessler COLM2026 and OPUS ICML2026 first. Kill if trivial composition or missing concrete advantage. Prefer a consequential system bottleneck with real benchmark and sufficiently novel algorithmic design. No GPU/Codex/training until PI permits. PI may instead PARK EAI-SYNTH and reallocate effort. Do not invent novelty.
All EAI-SYS (SCOUT-S54 and S55_NOT_STARTED), EAI-P, EAI-SEC and all FHE/SHIP/BOOT/CGS/VFHE/EXPLORE remain untouched and do NOT inherit this NEXT.


---

## LATEST OVERRIDING CHECKPOINT — SYNTH-C11 strategic stop gate (2026-10-26)

**TRACK_ID=EAI; ACTIVE_TOPIC=SYNTHETIC_DATA; ACTIVE_SUBLINE=EAI-SYNTH ONLY.**
**LATEST_COMPLETED=SYNTH-C11. NEXT_CANDIDATE=NONE_AUTOMATIC / SYNTH-C12_NOT_STARTED.**
**STATUS=FAIL_C11_SINGLE_FINAL_SFT_COST_EQUIVALENCE / STRATEGIC_REVIEW_RECOMMENDED.**
**NOVELTY=FAIL (C11 naive accounting/composition) / broad EAI-SYNTH NOT_ESTABLISHED.**
**STOP DECISION=AGENT_RECOMMENDS_PARK_C01_TO_C11; PI_REVIEW_REQUIRED, NOT UNILATERAL SWITCH.**

One source-first C11 hypothesis refuted: Kessler COLM2026 Algorithm1/§5.2 repeatedly refits a reinitialized student on growing teacher-generated cumulative data, while OPUS ICML2026 overhead 4.7% is relative to its own pretraining workload. Under explicit T rounds, m equal-size teacher samples per round, E student epochs per round, final-only student work EmT differs from actual total iterative refit work EmT(T+1)/2, ratio (T+1)/2; ten rounds 5.5× illustrative count, NOT measured Kessler GPU ratio. Kessler §5.4.2 Figure5 charges TEACHER input/output tokens as budget proxy, not student SFT and scoring all-in. Direct strongest prior art Yin–Rush `Compute-Constrained Data Selection` **ICLR2025** §4 explicitly jointly budgets C_v data selection and C_T finetuning and measures FLOP-quality Pareto across model sizes; therefore 'first unified selection+training budget' false. Merely adding teacher inference term to that budget is routine accounting, not a demonstrated new algorithm. OPUS+Kessler end-to-end improvements UNKNOWN; no native evaluation, no proof, no confirmed nontrivial technique.

**Detailed primary sources+single decisive computation:** `findings/eai-synth-c11-total-compute-budget-iterative-refit-strategic-gate-2026-10-26.md`.
**Negative archive:** `failures/eai-synth-c11-repeated-student-refit-cost-equivalence-no-go-2026-10-26.md`.
**NEXT_ACTION:** NO automatic C12 within this candidate series. Await explicit PI strategic decision to either park EAI-SYNTH current line or name a materially different source-supported synthetic-data mechanism with a smallest falsifiable new algorithmic claim and clear quality/compute advantage. If authorized, run exactly ONE gate, source-first, no GPU/Codex without separate approval. Do not launch another simple SGD/OT/verifier/EMA/budget toy. Root `STATE.md` near size limit, preserve existing file and use THIS modular state as source of truth.
**PENDING_CODEX:** `OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO`, carried and NOT_EXECUTED, NO prompts sent. No new C11 Codex.
**ISOLATION:** EAI-SYS latest SCOUT-S54/S55_NOT_STARTED, EAI-P, EAI-SEC, all FHE/SHIP/BOOT/CGS/VFHE/EXPLORE unchanged.
**STATE_UPDATE:** YES after exact GitHub reread.


---

## LATEST OVERRIDING CHECKPOINT — SYNTH-C12 cross-app causal state interface (2026-10-26)

**TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH ONLY.**
**LATEST_COMPLETED=SYNTH-C12. NEXT_CANDIDATE=SYNTH-C13_NOT_STARTED.**
**STATUS=FAIL_C12_APP_LOCAL_HISTORY_SUFFICIENCY / UNCLEAR_NEW_ALGORITHM.** Historical C01–C11 remain archived/PARKED (C11 strategic review recommendation not overruled). User "好的，请继续" after C11 authorized ONE fresh strategic research gate C12 within SYNTH, not an unlimited continuation or a switch to EAI-SYS/FHE. No Codex, GPU, model, environment or source code run.

**ONE C12 falsification:** For cross-app shared-resource contract, simulator of app B sees only same-app history and same request/schema/task/user; world W0 shared slot free vs W1 A has invisibly reserved the slot; correct `B.rooms.book(slot)` response must be SUCCESS vs CONFLICT. Identical B input means no B-only policy can guarantee correctness in both. This is an information insufficiency result, NOT real Apple measurement or any author's theorem error. Source Apple **SimSAT** Lee et al arXiv2607.16900v3 §3.3 PDF p5 explicitly restricts simulator history to prior SAME-APP API calls (original PDF screenshots p2 and p9); its work uses LLM judge/schema checks, and reports AppWorld/OfficeBench transfer. Source Gaia2 Froger et al **ICLR2026** https://arxiv.org/pdf/2602.11964 Appendix A.3 original PDF p18 screenshot explicitly says cross-app temporal/relationship/cross-modal constraints remain partly UNSOLVED in their app dependency graph. StateGen arXiv2606.16307v1 §4 uses global shared world-state manager, §12 admits multi-record transactions/partial rollbacks are uncertain; AWM ICML2026 and EnvFactory arXiv2605.18703 have executable/shared backend and dependency graph already. Generic share history/global state/event log is **OLD** and insufficient for publication. No new optimal bounded-context causal evidence projection, proof, code or benchmark is established.

**Novelty:** `FAIL` for obstruction/basic repair; `UNCLEAR / NOT_ESTABLISHED` for a narrowly costed **dynamic cross-app causal-state witness**, particularly temporal/transactional constraints at fixed simulation token/latency budget vs full global simulator. Original STS October2026 full text not yet accessible; verify before any future novelty claim. No actual SimSAT/Gaia2 training or consistency regression measured by us. A promising topic class is NOT an approved new algorithm.
**FULL EVIDENCE:** `findings/eai-synth-c12-cross-app-causal-state-local-history-source-gate-2026-10-26.md`.
**NEGATIVE ARCHIVE:** `failures/eai-synth-c12-app-local-history-cross-app-causality-no-go-2026-10-26.md`.
**NEXT_TEST (PI continuation ONLY):** ONE C13 strict source-first *method novelty and cost* gate: determine if proposed provenance-indexed minimal cross-app event/state projections with temporal contracts give verifiable lower prompt cost or stronger consistency than current Gaia2 global dependency graph, StateGen shared state, AWM/EnvFactory executable databases, classic event sourcing and incremental database views. Kill if generic event log already achieves same measurable goal. Do not restart C01–C11 toy sequence, no automatic C13/Codex/GPU.
**PENDING_CODEX:** OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO (carried, NOT_EXECUTED, prompt NOT_SENT); C12 no new Codex task.
**ISOLATION:** EAI-SYS SCOUT-S54/S55_NOT_STARTED, EAI-P, EAI-SEC, SHIP/BOOT/CGS/VFHE/EXPLORE all untouched. Do not write root STATE.md near size cap.
**STATE_UPDATE:** YES after exact reread.


---

## LATEST OVERRIDING CHECKPOINT — SYNTH-C13 causal projection classical IVM+SSI novelty gate (2026-10-26)

**TRACK_ID=EAI; ACTIVE_TOPIC=SYNTHETIC_DATA; ACTIVE_SUBLINE=EAI-SYNTH ONLY. LATEST_COMPLETED=SYNTH-C13; NEXT_CANDIDATE=SYNTH-C14_NOT_STARTED / NONE_AUTOMATIC.** Preserve B1–B12/C01–C12 and earlier parked sublines; EAI-SYS SCOUT-S54/S55_NOT_STARTED, EAI-P, EAI-SEC and FHE lines untouched. No Codex/GPU/training/model downloads/environment/source changes.

**ONE source-first H-C13 FALSIFIED:** Given a FULLY KNOWN shared relational cross-app contract with shared key u and deterministic predicates, compact per-request relevant state with correct incremental updates and concurrent booking safety NEEDS an original causal projection primitive beyond existing DB algorithms. FALSE. Encode occupancy as query Q_u=EXISTS active reservation on shared slot u; Noria OSDI2018 partial materialization and DBToaster PVLDB2012/DBSP VLDBJ2025 already incrementally maintain parametrized views/updates. Output to simulator just u and current Boolean (constant bytes for fixed-width u; key encoding O(log|U|) bits in general), not T prior events. Atomic check-and-insert inside serializable DB transaction via Ports–Grittner PVLDB2012 SSI enforces unique booking; ordinary Noria ALONE only has EVENTUAL consistency and does not suffice for this. Query payload bound is NOT a whole-system O(1) resource bound and not an auditable provenance witness. Cheney et al `Provenance as Dependency Analysis` already formalized dependency slicing and showed exact minimum dependency in their general query language is not computable. Agent-side Gaia2 ICLR2026, StateGen, AWM ICML2026 and EnvFactory supply global dependency/state/code-driven baselines. Prior source claims have exact reference and audit depth in finding. NO novel primitive or benchmark shown.

**STATUS:** FAIL_C13_NEW_CAUSAL_PROJECTION_PRIMITIVE_NECESSARY_FOR_FORMALIZED_RELATIONAL_CONTRACTS.
**RESULT:** Existing keyed IVM+serializable transactions solve C12 shared slot in restricted schema-known model; generic query-aware causal state prompt projection NOT novel.
**NOVELTY:** FAIL for proposed projection/basic fix; larger EAI-SYNTH NOT_ESTABLISHED.
**OPEN:** Inference, verification and cost-bounded acquisition of UNKNOWN cross-app shared keys/temporal/transactional contracts from textual OpenAPI and incomplete traces. This is not yet a constructed algorithm, and must be checked against program synthesis, text-to-DB, Gaia2, StateGen and executable agent environment generators. Avoid asserting universal exact minimal semantic witness.
**FINDINGS:** `findings/eai-synth-c13-causal-projection-ivm-serializable-priorart-gate-2026-10-26.md`.
**FAILURE:** `failures/eai-synth-c13-new-causal-projection-primitive-needed-no-go-2026-10-26.md`.
**NEXT:** No automatic C14. On explicit PI continuation, ONE truly distinct contract INFERENCE/VALIDATION gate, source-first before any Code/GPU; if only program-synthesis/DB reuse, recommend strategic PARK, not further elementary state-cache scans. PI retains decisions.
**PENDING_CODEX:** `OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO` carried and NOT_EXECUTED/NOT_SENT; C13 NONE.
**STATE_UPDATE:** YES if exact append readback.


---

## LATEST OVERRIDING CHECKPOINT — SYNTH-C14 execution-validated API dependency versus cross-app causal semantics (2026-10-26)

**TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH ONLY.**
**LATEST_COMPLETED=SYNTH-C14; NEXT_CANDIDATE=SYNTH-C15_NOT_STARTED / NONE_AUTOMATIC.**
**STATUS=FAIL_C14_SUCCESSFUL_WORKFLOW_IMPLIES_HIDDEN_CROSS_APP_CAUSAL_DEPENDENCE.**
**NOVELTY=FAIL** for treating API executable dependency inference as hidden causal/temporal business invariant discovery; wider SYNTH novelty `NOT_ESTABLISHED`. Historical B/C rounds preserved; EAI-SYS SCOUT-S54/S55_NOT_STARTED, EAI-P, EAI-SEC, FHE lines untouched. No Codex, GPU, model/training/remote operations.

**ONE H-C14 falsification:** A chain observed as `A.calendar.reserve(u)=SUCCESS, B.rooms.book(v)=SUCCESS` with `u≠v` has identical OpenAPI/positive trace in two possible worlds: W0 independent A and B slot inventories and W1 shared slot inventory. In unobserved same-key continuation `B.rooms.book(u)`, correct outcomes are SUCCESS W0 versus CONFLICT W1. So positive-only observed workflow executability cannot certify shared state dependence. This is elementary observational indistinguishability; requires control/reset/authorized targeted intervention and/or stronger specification to disambiguate. Does not invalidate authors' claimed results.

**Direct original strongest prior art and actual claim boundary:**
- Tu Nguyen et al `APIPilot` arXiv2608.17546v2 Aug20 2026 original https://arxiv.org/pdf/2608.17546 physical PDF page0 screenshot read; §III.D explicitly states successful 2xx certifies a producer-consumer dependency EXECUTABLE UNDER CURRENT CONTEXT, NOT full business correctness. APIPilot already proposes LLM/structural edge, concretely executes, forms workflow dependency graph and refines responses. 16-service 92.3% op coverage / 88.1% workflow success are author reported, NOT cross-app invariance metrics.
- Yang et al `LoBREST` arXiv2604.08007v1 original https://arxiv.org/pdf/2604.08007 physical p0 screenshot, §3–§4 parsed: business constraint inference from historical logs, locality slices, resource completion and fuzzing; no claim causal soundness for all hidden cross-app invariants. Formal venue unverified despite placeholder DOI.
- Khan et al `ARMeta` arXiv2605.28321v1 full original https://arxiv.org/html/2605.28321v1 §III seed/followup metamorphic pair execution, §V plans systematic CROSS-API consistency analysis; generic 'LLM propose contrastive API tests and execute' not novel.
- `CRUDinfer` ICSE2026 original conference https://conf.researchr.org/details/icse-2026/icse-2026-research-track/298/CRUDinfer-Automated-CRUD-Semantics-Inference-for-REST-APIs-Through-Black-box-Testing: black-box tests to refine CRUD semantics; exact published theorem not retrieved. RESTler ICSE2019 already discovered input/producer-consumer dependencies + dynamic response feedback.
**Only possible future direction (UNCONFIRMED):** Under authorized resettable multi-app sandbox, derive/test hidden SAME-ENTITY temporal/transactional constraints with matched counterfactual probes, measured oracle/side-effect/token budgets, strong relation soundness under nondeterminism; distinguish from existing ARMeta/APIPilot/RESTler, program synthesis and causality tests. NO original algorithm or gain yet. Avoid 'first discover API dependencies' false novelty.

**FINDING:** `findings/eai-synth-c14-executable-edge-vs-cross-app-causal-semantics-gate-2026-10-26.md`.
**NEGATIVE:** `failures/eai-synth-c14-executable-success-causal-cross-app-certification-no-go-2026-10-26.md`.
**NEXT:** NO AUTOMATIC C15. Only PI continuation permits one source-first constrained oracle/intervention-cost gate. If result just ARMeta/LoBREST composition, recommend PARK rather than more passive success toy tests.
**PENDING_CODEX:** `OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO`, unexecuted and no prompt released. No C14 Codex.
**STATE_UPDATE:** YES on exact append/readback. Root giant STATE.md NOT changed.
