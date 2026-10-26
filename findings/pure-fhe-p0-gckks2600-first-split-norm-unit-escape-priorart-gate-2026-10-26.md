# PURE-FHE · P0-PRESCOUT-26 — First-split integer-mask norm gate and cyclotomic-unit escape

DATE: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
LATEST_PREVIOUS: P0-PRESCOUT-25
STATUS: FAIL_FIRST_SPLIT_NORM_NO_GO / PASS_EXPLICIT_CYCLOTOMIC_UNIT_ESCAPE / UNCLEAR_TWO_LEVEL_GCKKS / SOURCE_BLOCKED_NOVELTY
NOVELTY: NOT_ESTABLISHED, strong overlap with Focused CKKS cyclotomic units
EXECUTION: paper/source checks, exact algebra and a local Sympy check of unit/resultant and embeddings, NOT a native FHE experiment.
OTHER_TRACKS: UNCHANGED, NO SHARED STATE.MD WRITE.

## 1. One falsifiable hypothesis H26

The first precision-doubling split in ePrint 2026/2600 (k=4→8) has no preexisting unused slots. Is that fact *alone*, together with integrality and the nonzero cyclotomic norm, sufficient to preclude an ordinary one-integral-mask / shared-power / two-Δ-rescale realization because the newly discarded slot mask must be O(1/Δ)?

Cheapest decisive test: derive the norm bound over ALL conjugate slots and test whether the required retained amplitude from exact F²→F' scale accounting violates it. Exhibit a real cyclotomic integer unit saturating the bound to falsify an overly strong no-go.

## 2. [FACT] Original source and source gaps

Primary supplied PDF papers/supplied/2026-2600.pdf blob 8db712155d087284d21e924623496bc48e36eb72 was independently reread via page-aware GitHub Notes PDF interface physical pages 18–21,25. §5.5 p25 explicitly starts split iterations at k=4, with usefulSlots=2N/k. Thus at k=4 it holds N/2 useful complex slots = the entire CKKS complex-slot capacity, with NO original unused slots. First split k=4→8 keeps N/4 and newly discards N/4 slots in each branch. §5.2 p19 chooses F' such that Δ'/c'_m≈Δ²/c_m²; original input CKKS has F=1,c_m=1, so Δ'/c'_m≈Δ² in this first split. Source has shared square/cube under F² before masks then F²→F' and a Δ³ rescale, and count of three Δ-sized levels. §5.2 p20–21 requires useful-slot correct scale and bounded newly-unused normalized noise |dout(η)|/|F'(η)|≤K.
Focused CKKS ePrint 2026/2531, Cheon–Lee revised Oct20, 2026: public title/abstract independently verified via eprint.iacr.asia/2026 but **FULL §6 PDF STILL NOT ACCESSIBLE**: supplied GitHub directory does not contain the file, ePrint 403 and other publicly searched routes yielded no authenticated full text. 2600 pp5–6 reporting two-level split-first Focused method is only secondary characterization. Dumezy ePrint 2026/2513 full paper also not independently read; however the Oct19 author's own blog https://jdumezy.com/blog/shaped-rounding/ explicitly discusses cyclotomic units, guard-slot shaping, conserved norm/product and close relationships among unit-based schemes including Focused CKKS. Do not imply unit shaping is novel.

## 3. [DERIVATION] General first-split nonzero integer mask norm bound

For N a power of two, ring R=Z[X]/(X^N+1) with N/2 conjugate pairs of primitive 2N-th roots. Let M∈R be a **nonzero** residue class and define A as an upper bound of |M(ξ)| for N/4 retained representative slots, and δ for N/4 newly discarded representative slots. Since X^N+1 is irreducible over Q, the resultant Res(X^N+1,M) is a nonzero integer. Taking product over all roots:
  1≤|Norm(M)|≤A^(N/2) δ^(N/2)=(Aδ)^(N/2).
Hence Aδ≥1. In particular, if A=O(1), δ=O(1/Δ) is impossible as Δ→∞, but the premise A=O(1) is NOT implied by GCKKS factor conversion and is false for the precise proposed scale balance below.

## 4. [DERIVATION] Why the first-split lower bound fails to kill a two-level attempt

Analyze ONLY P0-23's specified one-mask template: shared Y carries Δ² h1(x) under F², multiply by one integral selector-like M with retained amplitude λ, reinterpret as F', finally rescale by ρ. For retained value h1(1)=1, output Δ' requires
  λ=ρΔ'/(Δ²c'_m).
At new discarded slot with h1(1)=1, best-case zero-other-error normalization is |dout(η)|/|F'(η)|=(Δ²/ρ)|M(η)|, requiring
  δ≤Kρ/Δ².
At first split, c_m=1 and source chooses Δ'/c'_m≈Δ². Thus
  λ≈ρ,
not O(1). For ρ≈Δ, the target allows λ≈Δ and demands δ=O(1/Δ), so Aδ can be Θ(1). Consequently the first-split no-old-guards fact does NOT by itself disprove the two-level one-mask template; GCKKS factor/scale conversion changes the retained mask magnitude. This is a CONDITIONAL scale observation, not a constructive proof of all scale/noise correctness nor actual parameter existence.

## 5. [DERIVATION + TOY_EXECUTED] An exact unit saturates the norm lower bound

At N=8, define R=Z[X]/(X^8+1), U=1+X²−X⁶.
Sympy exact result (also elementary ring algebra):
  Res_X(X^8+1,U)=1,
  U^{-1}=-1+X²−X⁶ in R.
Canonical slots (conjugate representative exponents 1,9,5,13 for exp(πi/8)) give:
  U(ζ^1)=U(ζ^9)=1+sqrt(2)
  U(ζ^5)=U(ζ^13)=1−sqrt(2).
Thus for positive integer t, M=U^t has retained magnitudes A=(1+sqrt2)^t, newly discarded δ=(sqrt2−1)^t=(1+sqrt2)^(−t), so **Aδ=1** at all t. This explicitly falsifies 'integer masks cannot attain simultaneous large retained / tiny discarded values'. Powers U^t approximate a desired Δ contrast to within constant multiplicative factors at the slot-algebra level.
This is an explicit cyclotomic-unit mask and nothing more: it does NOT prove a correct GCKKS first precision-doubling algorithm, a valid target nonunit F', achieved precision, accumulated key-switch/rescaling noise, actual total modulus consumption or uniqueness. Its idea is substantially covered by existing Focused CKKS/unit-shaped rounding concepts.

## 6. Interpretation / priority

P0-23 proved a fixed small-λ rounded CRT-selector rewrite fails; P0-24 correctly gives a *conditional* old-guard amplitude lower bound; P0-25 showed nonunit F is not an integral unimodular change of coordinates. P0-26 corrects the possible overgeneralization 'no old guard => no two-level mask': the original Δ'/c'_m relation permits A=Θ(Δ), δ=Θ(1/Δ), a profile attained by cyclotomic units.
However this is NOT a genuine new construction, and the first split is exactly the unit-based competitor's known mechanism; any novelty must arise from correctly handling nonunit F²→F' at later rounds, not rediscovering a unit mask.
Repeated similar toy searches should stop after P0-26. User PI controls pivot. Absent independently read Focused §6, the existential shared-power 2-level novelty gate is SOURCE_BLOCKED/PARK and not implementation-ready. Reasonable next action: procure revised 2026/2531 original §6; compare precise nonunit conversion/noise and end-to-end cost. If unavailable, present value review or propose one independent promising GCKKS bottleneck with first-party evidence rather than continuing adjacent mask tweaks.

END_OF_ITERATION:
STATUS: FAIL_FIRST_SPLIT_NO_OLD_GUARD_NO_GO / PASS_UNIT_CONSTRUCTION / UNCLEAR_GENERAL_TWO_LEVEL_SOURCE_BLOCKED
RESULT: exact universal norm Aδ≥1 for first split, paper-specific λ≈ρ from Δ'/c'_m≈Δ², exact N=8 cyclotomic unit saturating Aδ=1; no validated FHE algorithm.
NOVELTY: NOT_ESTABLISHED / unit-shaping is prior art.
NEXT_TEST: Cheon–Lee 2026/2531 Oct20 revised full §6 primary text (not abstract or secondary 2600); compare split/mask/factor/noise; otherwise PARK and value/pivot review, not another toy.
STATE_UPDATE: YES — isolated PURE-FHE finding only, no shared STATE.md.
CODEX_REQUIRED: NO (implementation remains PENDING explicit PI approval).
