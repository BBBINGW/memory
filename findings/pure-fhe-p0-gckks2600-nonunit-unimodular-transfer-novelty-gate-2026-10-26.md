# PURE-FHE · P0-PRESCOUT-25 — Unit-lattice transfer gate and novelty/value review

Date: 2026-10-26 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-24, findings/pure-fhe-p0-gckks2600-mask-resultant-guard-budget-gate-2026-10-26.md (commit 461fdc99d9a69cb27c8019dd430405b323cde30c).
STATUS: FAIL_UNIMODULAR_TRANSFER_FOR_NONUNIT / UNCLEAR_SHARED_POWER_TWO_LEVEL / HUMAN_REVIEW_VALUE
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN. No GPU/remote server/native implementation.
OTHER_TRACKS: UNCHANGED.

## Single minimal technical hypothesis H25

Can the unit-based shaped/focused rounding change-of-basis technique be directly transferred to the nonunit GCKKS factor F, specifically at the F²→F' split-and-clean interface, as a zero-extra-cost bijection of the integer coefficient lattice, thereby bypassing P0-23/24's selector error?

Cheapest decisive test: compute the integral cyclotomic norm and rational inverse of a previously verified nonunit F and test unimodularity. In parallel, execute source-based novelty/value gate for shaped guard tradeoffs before proposing any more masks. This is an exact algebraic test, not a full scheme/noise proof.

## [FACT] Primary prior-art evidence/provenance

* User-supplied primary papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72, §4.1–4.4 pp13–17 and §5.2 pp19–21, §5.4 pp24–25: GCKKS authors explicitly allow nonunit decryption factors; share powers before splitting (3 scale-related levels), distinguish F²→F' factor reinterpretation during cleaning from separate final CKKS→GCKKS Algorithm1 requiring a small unreduced integer lift. The §5.2 source describes Focused CKKS revised tree as split-first, 2 levels per round, but this remains second-party attribution.
* Cheon–Lee, High-Precision CKKS with Focal Units, ePrint 2026/2531, publicly indexed revision Oct 20 2026; PUBLIC ABSTRACT only (https://eprint.iacr.asia/2026). Full revised PDF remains unavailable despite GitHub supplied listing, original ePrint HTTP403 via Notes, and public web/mirror/author-title lookup; do not infer §6 detailed algorithm.
* Dumezy, Fully Homomorphic Encryption for Small Batches of Complex Numbers, ePrint 2026/2513, author-first-party blog Oct19 2026 https://jdumezy.com/blog/shaped-rounding/ and publication page https://jdumezy.com/publications/new-scheme/ : author describes a unit g and shaped rounding g round(g^{-1}a/r), shaped errors small at data and amplified on guards, product-of-embeddings norm-one tradeoff, invariant guard noise and native bootstrapping, and explicitly says unit-shaped versions of his scheme, GCKKS and Focused CKKS relate through public coordinate transformations; GCKKS permits nonunit F. This is AUTHOR BLOG primary commentary, not independent peer-reviewed full-text theorem verification. Its first-party contribution already captures the generic 'move rounding noise to guards + norm constraint' rationale. Do not claim the exact P0-24 inequality appears in the Dumezy paper without its full text.

## [DERIVATION / EXACT SYMBOLIC TEST] Nonunit is not a unimodular basis change

In the toy cyclotomic ring R=Z[X]/(X^8+1), use the exact nonunit factor from earlier P0-21:
 F=3+X²−X⁶.
Sympy resultant/inverse calculation, independently recomputed in P0-25:
 Res_X(X^8+1,F)=2401=7^4;
 F^{-1}=(3−X²+X⁶)/7 in Q[X]/(X^8+1), and F*F^{-1}=1 in that quotient.
The quotient inverse is not in R. The map T_F:R→R by multiplication F has nonzero determinant norm(F)=2401, hence injective with lattice index [R:F R]=2401 and is **not** a bijection of the integer coefficient lattice. In contrast, multiplication by an integral unit g has |norm(g)|=1 and is a unimodular change of Z-basis. Therefore no direct equivalence 'ordinary integer coefficient rounding in a new integral basis of the same R' can be asserted with nonunit F.

Important domain caveat: for moduli Q coprime to 7, F may be invertible in R_Q because norm(F) is invertible mod Q; e.g., unit-lattice obstruction does NOT prove that a modulus-Q ciphertext conversion cannot be performed, nor an overhead lower bound for every scheme. A modular inverse is not itself a proof that integer rounding error profiles, useful-slot precision, nonunit F²→F' normalization or the GCKKS Lemma2 invariant are preserved. The source §5.4 already addresses nonunit CKKS→GCKKS via a new conditional component reencoding, so this elementary index proof is NOT itself a new contribution.

## [DERIVATION] Structural research-value conclusion

P0-23's simplest two-level 'share h1 then ordinary rounded mask and one final Δ divisor' fails new-unused leakage/correctness. P0-24's resultant A δ B1 B2≥1 supplies an exact precision/guard-amplification tradeoff under fixed old-guard budgets, but its conceptual direction is strongly overlapped by Dumezy's October 2026 explicit norm-one shaped-rounding guard tradeoff.
Unit shaping cannot automatically solve nonunit-F GCKKS: its integral-unimodular conjugacy fails at index 2401 toy. This isolates a real, source-supported nonunit interface difference. However 2026/2600 authors already know and address nonunit conversion, and without revised Focused §6 no evidence that a genuinely new, correct, noise-safe two-level algorithm remains.
Do not continue minor toy projector/rounding scans. This is the 3rd closely related pre-scout result without a constructed mechanism; initiate VALUE_REVIEW/HUMAN_REVIEW rather than scout inertia.

## Priority/value recommendation

(1) P0-25 closes direct integral-unit-transfer argument; no paper flaw or full FHE no-go.
(2) Hold general 2-level shared-power H23 as SOURCE_BLOCKED and PARK for novelty until full original 2026/2531 revision, preferably user-supplied papers/supplied/2026-2531.pdf. Obtain 2026/2513 original for detailed noise theorem if making claims beyond author blog.
(3) Only if source reveals a concrete nonunit-specific F²→F' composition obstruction not solved by Focused/shaped methods, define ONE new mechanism plus exact baseline, noise, scale, key switch and total modulus costs. Otherwise pivot this technical hypothesis.
(4) No Codex/native experiments on this unverified novelty target. Any later implementation needs explicit PI authorization.

END_OF_ITERATION:
STATUS: FAIL_UNIMODULAR_TRANSFER_FOR_NONUNIT / HUMAN_REVIEW_VALUE (GENERAL_TWO_LEVEL_UNCLEAR)
RESULT: Exact toy F norm 2401/index 2401/rational inverse denominator 7; direct unit-shaped basis transfer invalid at integer-lattice level; Dumezy first-party disclosures make generic guard/norm result prior-art-heavy.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: FIRST get and read Cheon–Lee revised 2026/2531 §6 original PDF for split masks, two-level scale/noise and actual prior-art mechanism; without it prepare bounded pivot/value review, not another analogous toy.
STATE_UPDATE: YES — isolated PURE-FHE finding only; do not edit shared STATE.md or other tracks.
CODEX_REQUIRED: NO; eventual native implementation PENDING explicit PI approval.
