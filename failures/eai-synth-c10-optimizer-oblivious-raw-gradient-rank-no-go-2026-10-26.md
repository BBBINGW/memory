# EAI-SYNTH C10 negative — Raw-gradient selection ranking need not equal preconditioned one-step loss ranking
2026-10-26 Asia/Singapore. TRACK_ID=EAI, ACTIVE_SUBLINE=EAI-SYNTH only; one PI-authorized mathematical/prior-art gate. B11/B12 He semantics and C01–C09 previous archives untouched. No Codex/GPU/training/models/remote server.

[H-C10 FALSE] For fixed real target and candidate synthetic gradients, raw Euclidean gradient alignment preserves actual post-update real-loss-decrease ranking under every positive, non-scalar frozen optimizer preconditioner. Counterexample:
 L_R(theta)=.5||theta||², theta=(1,1), g_R=(1,1), D=diag(4,1), eta=.1.
 g_A=(0,2), g_B=(1,0).
 Raw U_A=2>U_B=1 but induced U_D,A=2<U_D,B=4.
 theta'_A=(1,.8), L_A=.82, Delta_A=.18.
 theta'_B=(.6,1), L_B=.68, Delta_B=.32.
 Thus RAW ranks A, actual descent B; exact no approximations. For 0<eta<1/3, Delta_B−Delta_A=2eta−6eta²>0.
 D is frozen *AdamW-like local linear geometry*, NOT an exact all-state AdamW update nor claim of an actual FROST run.

[STRONG SOURCE NOVELTY KILL]
- Wang et al, OPUS, ICML2026 official PMLR306 https://proceedings.mlr.press/v306/wang26gc.html : optimizer-induced projected utility, AdamW/Muon, Ghost+CountSketch, Boltzmann diversity, author reports +4.7% extra compute. Authors project https://yancyou.github.io/OPUS_page/ and public original preprint text https://www.researchgate.net/publication/400505961_OPUS_Towards_Efficient_and_Principled_Data_Selection_in_Large_Language_Model_Pre-training_in_Every_Iteration Eq(19)–(21)/Algorithm1 inspected, includes P_t grad L and update space <g_val,P_t grad_z>. Final official PDF linked via Github raw but direct web PDF fetch blocked; no claim of its pages visually validated. Proposed 'optimizer awareness' and gradient sketch mechanism are directly existing methods, not ours.
- Kessler et al, 'Towards Active Synthetic Data Generation for Finetuning Language Models', COLM2026 per Microsoft; full author arXiv2512.00884v2 original PDF https://arxiv.org/pdf/2512.00884 physical p4 and p6 visually checked: Algorithm1 iterates student-driven high-loss/uncertainty selection, teacher synthetic generation under fixed samples / teacher compute budget, reinitializing student SFT; §5 4 reasoning datasets/4 models. Simple cheap acquisition often competitive with LLM-as-a-judge, direct closed-loop generation prior art. Different from OPUS optimizer-aware pretraining, NOT a single already-integrated theorem.
- FROST arXiv2609.29988v1 original https://arxiv.org/html/2609.29988 §3.1 uses raw real-gradient/ synthetic-gradient alignment for mixed training; no proof raw scores preserve every modern optimizer risk ranking, so this is NOT an author theorem bug.

[RESULT] Important optimizer ranking interface is correct mathematically but **no new contribution**: direct published OPUS already optimizes it with efficient projected computation; student-budgeted synthetic generation also prior existing. No joint costed FROST/OPUS/Kessler method or end-to-end Pareto improvement demonstrated. Do not transfer OPUS 4.7% pretraining overhead and 0.5B-vs-3B CPT gain to synthetic teacher-generation SFT. This example does not establish actual finite-model regression performance or practical ranking reversal frequency.

STATUS: FAIL_C10_RAW_GRADIENT_ALIGNMENT_RANK_EQUIVALENCE_UNDER_PRECONDITIONER
RESULT: Exact 2D quadratic optimizer-aware ranking reversal, strong direct ICML2026 prior art.
NOVELTY: FAIL; EAI-SYNTH overall NOT_ESTABLISHED.
NEXT_TEST: No automatic C11. PI may choose one strategic literature-first gate whether truly JOINT teacher generation + optimizer-aware filtering has a costed/novel irreducible obstruction; if only OPUS+Kessler composition, PARK and consider a new EAI research program.
PENDING_CODEX: Carry OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO, NOT_EXECUTED/NOT_SENT; C10 NONE.
STATE_UPDATE: YES after exact file and modular state readback.
