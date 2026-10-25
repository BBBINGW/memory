# EAI-SYNTH B12 negative — Later author source did not disambiguate Sparse Counting noise lifetime
2026-10-25, TRACK_ID EAI / ACTIVE_SUBLINE EAI-SYNTH only. No Codex/training/GPU.

H-B12 [UNVERIFIED / NEGATIVE]: Later canonical author source resolves B11's repeated-timestamp lambda'_t sampling lifetime, provides a hard segment-index cap and lets us classify the 2024 algorithm as correct or faulty.

SOURCE FIRST:
1. 2024 paper formal IEEE Transactions on Privacy 1:19–30 DOI 10.1109/TP.2024.3486687 (author publication list). arXiv2402.08012v3 PDF original https://arxiv.org/pdf/2402.08012, Algorithm2 physical PDF p6 screenshot and Appendix A p19 screenshot. Sparse loop checks before record consumption, and under rare noise may close empty segment with unchanged t; Appendix A assumes a total of 2T Laplace noise variables and trivial T segment bound even on bad event.
2. NEW, independently authored 2025 doctoral dissertation by the first author Yiyun He, official UC Irvine eScholarship https://escholarship.org/uc/item/8pg3c2md and PDF https://escholarship.org/content/qt8pg3c2md/qt8pg3c2md.pdf . Chapter5 §5.2.2 Algorithm10 PDF physical p93 (printed p82), Lemma5.6 proof p94–95. PDF text clearly retains pretest-before-input; `lambda'_t~Lap` inside condition; unconditional 2T-noises/T-segments proof language. Neither PDF precisely defines whether SAME t retries redraw or reuse lambda'_t. Source PDF text fetched; image screenshot on publisher PDF failed HTTP429 (do not claim visual confirmation).
3. Author-hosted article PDF indexed with same Algorithm2 text: https://www.math.uci.edu/~rvershyn/papers/hvz-online_differential_privacy.pdf . Direct host PDF download returned 502 and final typeset IEEE article inaccessible; no independent canonical code or erratum verified in limited web/GitHub repository discovery.

ONE decisive comparison: author's later Algorithm10 repeats the exact ambiguous loop and no explicit noise-lifecycle rule; this REFUTES the notion that the later author source *settles* B11, but establishes neither intended sampling semantics nor a deployed bug. Two hypothetical B11 calculations remain conditional: fresh per-test draw ⇒ standard geometric expected retries; time-t reused test noise with fresh segment thresholds ⇒ mathematically infinite expected retry draws due to matched exponential tails. Do not assert the latter for the unresolved author mechanism.

STATUS: HUMAN_REVIEW_B12_SOURCE_SEMANTICS_UNRESOLVED
RESULT: Confirmed text-level persistence in a newer 2025 author thesis, missing implementation/author clarification. PARK subline; no reason for repeated toy scans.
NOVELTY: NOT_ESTABLISHED; not a new cryptographic/privacy vulnerability or publishable primitive.
NEXT_TEST: Only if PI supplies/authorizes direct authoritative final-paper code or version verification; alternatively pivot to another independently specified synthetic-data hypothesis on PI instruction.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO; carried without execution or instructions.
STATE_UPDATE: YES after GitHub exact readback and root STATE append.
