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
