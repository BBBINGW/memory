# EAI-SYNTH C16 NEGATIVE — unknown cross-app action synchronization has direct CONCUR 2025 prior art
Date: 2026-10-26 Asia/Singapore | TRACK_ID=EAI | EAI-SYNTH only.

ONE PRIMARY CLAIM FALSIFIED: In a resettable deterministic multi-app system with finite known GLOBAL API-action labels and observed SUCCESS/REJECT trace membership, inferring hidden cross-app state synchronization/alphabet decomposition with efficient component learning NECESSARILY requires a new algorithm beyond classical compositional active learning.

ONE FIRST-PARTY THEOREM + REPRESENTABILITY FALSIFIER:
Henry–Mousavi–Neele–Sammartino, **Compositional Active Learning of Synchronizing Systems Through Automated Alphabet Refinement**, CONCUR2025 DOI 10.4230/LIPIcs.CONCUR.2025.20, ORIGINAL PDF text https://tneele.com/static/papers/concur2025_comp_learning_alphabets.pdf ; §3.1 Def3.3/3.4 synchronized parallel LTS, §4 Thm4.25 finite refinement, §5 Algorithm1/Lemma5.1/Thm5.3 correct termination under ideal membership/equivalence teacher; **Remark5.4 disclaims recovering physical component number/identities**. Original PDF text available; visual screenshot attempt failed, no figure image verified.

Let a=A.reserve(u), b=B.book(u), success-only trace alphabet. Independent inventory: Σ_A={a}, Σ_B={b}, both local enabled => global ab enabled. Shared-inventory coupling: Σ_A={a}, Σ_B={a,b}; B-associated LTS transitions q0 -a-> q1, q0 -b->q0, no b from q1. Event a is simultaneously a public A action and an abstract update to B-associated component, though NO call to B necessarily occurs at that moment. Thus a,b individually enabled while ab is not. Starting singleton alphabet distribution {a},{b}, the spurious predicted ab is a global negative counterexample and the existing CoalA distribution refinement can merge/constrain alphabet membership to capture it. The learned LTS need not reflect actual service decomposition or causal physical architecture. This is a restricted trace-language encode; it is NOT full business API semantics, token/side-effect bounded discovery or async serializability.

Nearby strong sources: C15 original SL^lambda JAR2026 handles active equality guard learning; FDRRestTest ESEM2026 official **abstract only** https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.20 already combines dynamic API dependency, logical oracle and budget-aware test scheduling. Thus no new 'first graph refinement/budgeted feedback' claim.

No physical API calls, code, Codex, GPU, model training or remote tests. No new nontrivial repair algorithm has been established for stochastic, timed, concurrent, irreversible or opaque identity-mapping regimes. CoalA MAT theorem uses ideal equivalence queries; real finite-budget certification not implied. C13-C16 four negative gates suggest strategic PI PARK or *materially distinct* source-supported task rather than C17 adjacent toy.

STATUS: FAIL_C16_NEW_UNKNOWN_SYNCHRONIZATION_ALPHABET_DISCOVERY_NECESSARY
RESULT: Unknown action synchronization in finite LTS is already learnable using CoalA and counterexample-guided alphabet refinement; hidden shared-store behavioral inhibition representable as existing synchronized LTS.
NOVELTY: FAIL restricted claim; full EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: NONE_AUTOMATIC. PI decides PARK / substantial reformulation. C17_NOT_STARTED.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO remains PENDING, previously displayed, not confirmed executed. No C16 Codex.
STATE_UPDATE: YES after GitHub readback.
