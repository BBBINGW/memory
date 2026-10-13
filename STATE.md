# FHE Research State — After Iteration 155

**Checkpoint:** 2026-10-13 · `main` · I155 completed, I156 **NOT STARTED**.
**Authority:** This file is a compact recovery entry point, not a history log. The former full 84,552-character `STATE.md` is preserved verbatim at `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`). Long-term directions and archives are indexed in `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI makes direction, continuation, novelty and disclosure decisions.

## CURRENT TARGET

**Research direction (OPEN/HUMAN_REVIEW; no ACTIVE experiment):** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, **IACR ePrint 2025/286**. Audit/possible low-cost repair for **global diagonal integer scalar-digit lookup across CRT field components** in §4.3 Theorem 4.8 / §5 Brakedown PCS. Primary full 52-physical-page PDF was read through Research MCP from a GitHub mirror (PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`); equality to the latest official revised ePrint PDF remains **VERSION_UNVERIFIED**. Relevant source: §3.1, §4.3 physical pp20–23, §5 pp25–26, Appendix F.2/F.3 physical pp50–52. Original author public code: `vfhe/proof-friendly-CKKS`.

## LAST COMPLETED ITERATION

**155 (2026-10-13)**; **I156 NOT STARTED.** PI assented to stopping repeated integer code variants and testing whether the current official 2026-02-16 revised ePrint PDF can be verified to match I59–60's 52-page mirror. I155 **UNCLEAR / MISSING_CURRENT_OFFICIAL_BINARY**: official landing confirms the revision date, but its actual current PDF bytes could not be retrieved/hashed and compared. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md`.

## CURRENT QUESTION

Parent P1 **OPEN/HUMAN_REVIEW / SOURCE-GATED**: does vFHE's Theorem 4.8 and its composed range PIOP in the **actual latest official revised version** still fail to constrain diagonal scalar digits across CRT components? I59–60 established an ideal-PIOP/abstract composition counterexample **in inspected 52-page GitHub-mirror PDF**, not against a byte-confirmed current official edition or a compiled SNARK. I152–154 integer-encoder replacement attempts are **PARKED by PI decision** after three distinct source-distance failures. **No active experiment or alternative research direction.**

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I155 test hypothesis that today's official ePrint PDF is the 52-page mirror (or contains the same Appendix E.2 diagonal-vs-componentwise step): **UNCLEAR**, no current official PDF raw bytes acquired. Official landing currently lists 2026-02-16 revision explicitly fixing an earlier Theorem 4.8 proof flaw, but web PDF index returns a 50-page OLD cached copy; Research MCP mirror (52pp, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`) still includes Theorem4.8 `β<pmin,2^ell*<pmin`, Remark4.9 (p24) and the disputed Appendix E.2 CRT projection inference (p48). Version identity remains `VERSION_UNVERIFIED`; **do not assert latest official-source defect**. Critical original binary source request in `MISSING_SOURCES.md`.

## CURRENT EVIDENCE

- **[I155 UNCLEAR / SOURCE GATE]** Official `https://eprint.iacr.org/2025/286` landing lists 2026-02-16 revision to Theorem 4.8 proof. Exact official current PDF bytes unavailable; web's 50pp cache conflicts with Research MCP's 52pp mirror, which has revised Remark4.9 and still contains invalid diagonal⇒fieldwise membership inference on physical p48. Identity NOT proven, no official exploit conclusion. Evidence `findings/vfhe-current-official-revision-identity-gate-iteration155.md`; source request `MISSING_SOURCES.md`.
- **[PI PARK DECISION]** I152 single-flip Hadamard, I153 tensor multi-flip Hadamard and I154 cyclic-window integer encoder fast repair approaches are **PARKED** after independent source-distance obstructions. Parent P1 remains OPEN/HUMAN_REVIEW; no coding variants without new PI decision.
- **[DERIVED/EXACT I154; NEGATIVE]** Source-compatible `m=N=256,d=4,p=(641,1153)`. Sliding-window integer code with 64-term parity windows has common integer honest values and `O(m)` encoding; however `(1-X) f_L=1-X^L` makes a weight4 codeword, vs F.3 RS exact distance65. Universal `δ≤2/m`; this is local cancellation and independent of the prior Hadamard obstructions. Archive `failures/vfhe-cyclic-window-integer-encoder-local-cancellation-iteration154.md`.
- **[DERIVED I153; NEGATIVE]** Multi-flip/tensor Hadamard has `dmin≤2√m`, `δ≤1/√m`, and at m256 exact witness weight32 < RS65. `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md`.
- **[DERIVED I152; NEGATIVE]** One-coordinate-sign-flip Hadamard exact `dmin4` all m power-of-two ≥4. `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md`.
- **[DERIVED I151; NEGATIVE]** Original per-prime native RS code columns cannot be compared as common bounded integers even on honest inputs: toy source-root j1 values 12 vs 6. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`.
- **[DERIVED I59–60; HUMAN_REVIEW]** Ideal PIOP-level and abstract composition CRT *diagonal scalar-digit* issue; not a verified latest-official-version defect or compiled end-to-end SNARK forgery. `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`.
- **[FACT]** Original paper ePrint 2025/286 §3.1, §4.3, §5, Appendix F.2/F.3 (physical pp51–52 latest re-read): F.2 uses Merkle-authenticated row-encoded columns; F.3 uses native-field RS `[N/2,N/4,N/4+1]`. Full 52-page PDF from GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** against official most recent revision. Formula extraction warning. Author NTT benchmark `vfhe/proof-friendly-CKKS/lib/main_benchmark.cpp` SHA `f92e054ae758ddf3c35e22d1a0294374ef2d6b3e`.
- **[PARKED]** I95 expensive direct Brakedown, I136–138 PCS micro-batching, I148 masks small gain, I149/150 one-point integer lifts blocked. See `findings/OPEN_RESEARCH_BRANCHES.md`. Previously reported strict `p<2^49` is a conditional simplification (some source primes exceed).

## MAIN OBSTRUCTION

**Highest priority source obstruction:** official Feb 2026 ePrint PDF cannot be byte-identified with the 52-page cached GitHub mirror. I59–60's implication fails algebraically in the inspected mirror, but full current official-version applicability and compiled proof impact remain UNVERIFIED. Independently, unchanged source F.3 RS is prime-dependent (I151); three new cheap integer encoder attempts I152–154 fail to maintain its distance. **Integer encoding replacement is PARKED; no new repair or attack established.**

## OPEN UNCERTAINTY

**[OPEN / SOURCE-GATED]** Current official PDF SHA and contents, possible further official constraints, end-to-end compiled/Fiat–Shamir proof impact, research novelty/priority, author-confirmed status. No disclosure or security claim permitted. Other historical failure archives not reopened.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**ONE EXECUTABLE SOURCE GATE; I156 NOT STARTED.** Retrieve the exact **current official** PDF raw bytes for ePrint 2025/286 (2026-02-16 revision) using a verified download or PI-supplied `papers/supplied/` file; pin SHA256 and compare to mirror `29b6b2e9…`. If different, read the official §4.3 Theorem4.8, Remark4.9, Appendix E.2 and §5, testing whether the CRT-diagonal implication and absence of cross-prime index binding persist. If source still inaccessible, stop and report **MISSING CRITICAL SOURCE**, rather than another inconclusive iteration. Do NOT resume coding variants, pivot, or contact authors without new PI instruction.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this file.
2. `findings/vfhe-current-official-revision-identity-gate-iteration155.md` — latest verified/unverified boundaries and official-source acquisition gate.
3. `MISSING_SOURCES.md` — requested official PDF bytes and source resolution instructions.
4. `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — underlying I59–60 mirror-backed abstract finding.
5. `findings/OPEN_RESEARCH_BRANCHES.md` — durable index.
6. `failures/vfhe-cyclic-window-integer-encoder-local-cancellation-iteration154.md`, `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md`, `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md` — PARKED code variants (read only if needed).

## STATUS

**I155 CLOSED: UNCLEAR / MISSING_CURRENT_OFFICIAL_BINARY.** Latest official landing revision 2026-02-16 CONFIRMED; cached 52pp mirror has disputed Appendix E.2 step, but official-current PDF SHA NOT VERIFIED. Parent P1 CRT scalar consistency OPEN/HUMAN_REVIEW / SOURCE-GATED; integer-encoder fast repair I152–154 PARKED on PI assent; no active experiment; **I156 NOT STARTED**. Next is single official-PDF raw-source gate, or STOP if inaccessible. No outreach/disclosure.
