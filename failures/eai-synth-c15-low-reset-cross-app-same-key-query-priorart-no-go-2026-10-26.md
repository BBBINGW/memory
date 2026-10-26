# EAI-SYNTH C15 NEGATIVE — low-reset cross-app same-ID query-selector not novel under RA model
Date: 2026-10-26 Asia/Singapore | TRACK_ID EAI | EAI-SYNTH only.

ONE PRIMARY HYPOTHESIS FAILS: For a RESETTABLE DETERMINISTIC black-box pair of services with finite control, one stored resource ID, equality/inequality guards, and sequential order rules, short budgeted same-ID vs different-ID interventions to discover hidden cross-app success/conflict constraints require a new active causal test-selection algorithm.

ONE decisive SOURCE/REPRESENTABILITY test: A.reserve(x) stores register r=x (q0→q1); B.book(y) in q1 branches y=r or y!=r; shared-inventory CONFLICT vs independent-inventory SUCCESS on y=r. This is a one-register automaton/data-language with finite control. Dierl et al., **SL^lambda: A Scalable Algorithm for Register Automata Learning**, Journal of Automated Reasoning 70:14 (2026), full original https://link.springer.com/article/10.1007/s10817-026-09758-9 §4 and §7, already infer such equality guard dependencies using short restricted distinguishing suffixes. §6 Theorem 1, Theorem 7, Corollary 8 bound ideal-oracle learning, with O(t) equivalence queries and O(t²(2n)^n + mt² m^m) membership queries in equality theory. §8 uses actual reset metrics. NOT a proof that real black-box equivalence or any joint reset/token/side-effect budget is satisfied.

NEIGHBORING PRIOR: **ARMeta**, full original https://arxiv.org/html/2605.28321v1 §III-B explicitly budgets total API requests and time for executable seed/follow-up metamorphic testing; §IV-B author's 1000 requests/30min; §V systematic cross-API consistency acknowledged as future work. **AutoRestTest** ICSE2025 institutional abstract and **BRAT** ICSE2026 SEIP conference abstract both do adaptive dependency-driven test exploration, not verified full hidden-causal contracts. Earlier C14 APIPilot, RESTler, LoBREST and CRUDinfer foreclose generic dependency novelty.

LIMITS: Does NOT cover arbitrary hidden identity translations, unbounded simultaneous shared keys, clocked events, concurrent transaction rollback, nondeterminism, incomplete reset, irreversible effects, or joint vector costs; NO new complete repair or result for them, and no original API/GPU/code tests. Our single-register RA reduction is NOT a universal multi-app semantics guarantee, and no existing paper is accused of an error.

STATUS: FAIL_C15_LOW_RESET_CROSS_APP_EQUALITY_PROBING_VS_REGISTER_AUTOMATA
RESULT: Restricted proposed new low-reset interventional causal selector reduces to already-optimized active RA learning.
NOVELTY: FAIL for restricted selector; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: NONE_AUTOMATIC. Recommend PI strategic PARK/review after C13/C14/C15; C16_NOT_STARTED.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO still pending; prior ChatGPT supplied prompt but execution never verified.
STATE_UPDATE: YES after finding, failure and modular state verified; root STATE.md and all unrelated tracks unchanged.
