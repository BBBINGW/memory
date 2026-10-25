# EAI-SYNTH B7 negative — Original per-window 1/H good events do not naively give a high-confidence global tree event
Date: 2026-10-25. TRACK_ID EAI / ACTIVE_SUBLINE EAI-SYNTH only. No Codex/GPU/training/source changes.

H-B7 [FALSE]: Directly union-bounding unmodified Algorithm2 Appendix-A per-window threshold-noise good-event failures 1/H across all He Algorithm1 spatial cells and Algorithm3 time epochs gives o(1) failure for simultaneous full-tree noise accuracy, sufficient to plug into high-prob W1.
Single source-first decisive calculation [DERIVATION]:
He arXiv2402.08012v3 https://arxiv.org/html/2402.08012v3 §§3.2–3.4, 4.1–4.2 Eq4.1/4.4–4.7, Appendix A: time-level i lasts H_i=ceil(2^(i+1)/epsilon)-ceil(2^i/epsilon)~2^i/epsilon; all depth j=1,...,i cells are active (2^j each), so M_i=2^(i+1)-2. If each subroutine only carries its original Appendix-A threshold-good-event failure upper bound 1/H_i, the union-bound expression at one epoch is M_i/H_i=Theta(epsilon). Across i=1,...,r it is Theta(epsilon*r), which is vacuous for fixed epsilon and growing r; it cannot certify failure o(1). EXACT example epsilon=1, H_i=2^i gives sum_i M_i/H_i=2r-2(1-2^-r), r=5 -> 8.0625 and r=10 -> 18.001953125. THESE VALUES ARE ONLY UNION-BOUND EXPRESSIONS, NOT ACTUAL FAILURE PROBABILITIES OR LOWER BOUNDS.
This refutes only one obvious proof tactic; cells' failures need not be independent, and weighted W1 may be accurate even if not all counter noise-good events hold. Lemma4.2 is an expectation statement, not source proof of high-prob pathwise W1. A stricter beta-allocation or correlated/weighted concentration could close the proof; original threshold T0=9log H/eta versus required noise envelope 2B(beta) must be tested before claiming direct repair or a real obstacle.

STATUS: FAIL_B7_NAIVE_UNMODIFIED_GLOBAL_UNION_CONFIDENCE
RESULT: Multi-cell event counting defeats the *unmodified direct union-bound certificate*; neither He algorithmic utility loss nor publishable theorem established.
NOVELTY: FAIL for claimed simple transfer; broader topic NOT_ESTABLISHED.
NEXT_TEST: Only upon PI authorization for B8, calculate with original threshold constant/actual per-cell confidence whether strengthened simultaneous event still guarantees positive-mass segments; one cheapest derivation, no code.
PENDING_CODEX: NONE_REQUIRED_FOR_B7; hold all future Codex requests until explicitly requested.
STATE_UPDATE: YES only upon GitHub write/readback and root STATE checkpoint verification.
