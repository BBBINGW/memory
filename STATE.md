# FHE Research State — After Iteration 153

**Checkpoint:** 2026-10-13 · `main` · I153 completed, I154 **NOT STARTED**.
**Authority:** This file is a compact recovery entry point, not a history log. The former full 84,552-character `STATE.md` is preserved verbatim at `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`). Long-term directions and archives are indexed in `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI makes direction, continuation, novelty and disclosure decisions.

## CURRENT TARGET

**Research direction (OPEN/HUMAN_REVIEW; no ACTIVE experiment):** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, **IACR ePrint 2025/286**. Audit/possible low-cost repair for **global diagonal integer scalar-digit lookup across CRT field components** in §4.3 Theorem 4.8 / §5 Brakedown PCS. Primary full 52-physical-page PDF was read through Research MCP from a GitHub mirror (PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`); equality to the latest official revised ePrint PDF remains **VERSION_UNVERIFIED**. Relevant source: §3.1, §4.3 physical pp20–23, §5 pp25–26, Appendix F.2/F.3 physical pp50–52. Original author public code: `vfhe/proof-friendly-CKKS`.

## LAST COMPLETED ITERATION

**153 (2026-10-13)**. **I154 NOT STARTED.** I153 was narrowly authorized by the PI's “好的，请继续” following I152; a distinct many-flip tensor/quadratic-sign Hadamard encoder failed source-comparable distance. See latest failure file below.

## CURRENT QUESTION

Can a genuinely **nonseparable/non-tensor** fast field-independent bounded-integer linear encoder make already-authenticated Brakedown F.2 **testing-phase Merkle columns** certify common CRT scalar digits without new costly native MLE evaluation-phase openings **while retaining F.3 source-comparable minimum distance**? I152 one-flip and I153 multi-flip tensor-Hadamard candidates are both closed by low-weight codewords. Parent P1 remains OPEN/HUMAN_REVIEW; **no new candidate is authorized/selected**.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I153 [NEGATIVE/FAIL candidate at source-compatible size]: for `Enc(x)=(H_m x,H_m D_m x)`, `m=4^t`, `D_m=diag(1,1,1,-1)^{⊗t}`, a tensor-eigenvector has codeword weight `2√m`; at `m=N=256,d=4,p=(641,1153),beta=2`, exact weight **32**, versus original F.3 `[512,256]` piecewise-RS minimum distance **65**. Relative distance upper bound `1/√m→0`. Honest beta2 centered integer no-wrap PASS, but no source-equivalent code distance. Distinct from I152's single-coordinate flip. Full details: `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md` SHA `b36878bc9937591a59daa467092e769ddee51138`.

## CURRENT EVIDENCE

- **[DERIVED/EXACT I153; NEGATIVE scalable encoder]** In a source-compatible `N=m=256,d=4`, odd-a primes 641/1153, original F.3 direct-sum RS `4×[128,64,65]` has `[512,256]` minimum distance 65. Candidate quadratic/tensor sign `D=(1,1,1,-1)^{⊗4}` (120 negative diagonal signs) has an **explicit valid field codeword of weight 32**, although centered honest `beta=2` integer outputs are bounded by 256 < 641/2. For `m=4^t`, tensor-fixed vectors give `dmin≤2√m`, relative `≤1/√m`. This is a field-code distance falsifier, not an actual digit-bound cheating transcript or proof-system attack. See `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md`.
- **[DERIVED/EXACT I152; NEGATIVE scalable encoder]** Single-coordinate-flip `D` has exact `dmin=4` over all `m=2^k≥4` odd-characteristic fields (toy `m=4,p=29,37` distance/no-wrap PASS); relative `2/m→0`. See `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md`.
- **[FACT]** Source F.2 commits row-encoded matrices as Merkle column leaves; testing opens columns and evaluation sends separate vectors. F.3 uses per-prime native-field Reed–Solomon NTT encoding. Author `vfhe/proof-friendly-CKKS/lib/main_benchmark.cpp` SHA `f92e054ae758ddf3c35e22d1a0294374ef2d6b3e` realizes coefficient-to-root RS encoding.
- **[DERIVED I151 FAIL existing native RS comparison]** Common honest scalar x=(0,1) yields source-root RS symbols 12 vs 6 at the same j1 for F29/F37; unchanged Merkle code columns cannot be compared as one small integer. See `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`.
- **[DERIVED I59–60; HUMAN_REVIEW]** Ideal PIOP-level CRT scalar-index coherence soundness counterexample and full abstract composition audit, NOT a verified full compiled SNARK exploit/latest official revision defect. See `findings/vfhe-crt-lookup-cross-component-soundness.md`; `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`.
- **[PARKED]** I95 direct Brakedown expensive; I136–138 native PCS fold shortcuts fail; I148 mask-only small gains; I149/150 existing MLE opening integer lift fails completeness or single-point soundness. See `findings/OPEN_RESEARCH_BRANCHES.md`.
- **[SOURCE CAUTION]** Original 52pp ePrint 2025/286 GitHub-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19` remains **VERSION_UNVERIFIED** versus latest official revision. Author IFMA sample primes can exceed `2^49`; old literal strict small-prime inequalities are conditional approximations.

## MAIN OBSTRUCTION

Old F.3 native RS is **field dependent**, making direct honest cross-CRT integer comparison false (I151). Two distinct fast signed-integer Hadamard pairs have **vanishing relative code distance**: single-flip I152 `2/m`, quadratic/tensor many-flip I153 `≤1/√m`, despite toy honest no-wrap. Need a genuinely different **nonseparable** bounded-integer, source-comparable high-distance encoder before proposing PCS reuse; F.2 testing/commitment soundness, proof binding, Fiat–Shamir privacy, 128-bit query parameters and concrete cost are all unproven. **No repair exists yet.**

## OPEN UNCERTAINTY

**[OPEN]** Existence and novelty of a non-tensor near-linear bounded-integer high-distance code valid over all native CRT fields; honest digit no-wrap at actual parameters; proof that authenticated shared testing Merkle columns enforce global diagonal scalar-digit indices without unacceptable overhead. Latest official PDF equality and actual compiled SNARK effect of I59–60 still unverified. All previous failure archives remain parked unless new premises emerge.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**HUMAN PI DECISION REQUIRED; I154 NOT STARTED.** Choose **one**: (a) PARK the two-attempt Hadamard/integer-encoder repair line and retain the parent P1 vFHE issue for later; or (b) explicitly authorize **ONE genuinely different nonseparable / non-tensor field-independent integer-code candidate**, predeclaring `d_min≥65` at `N=m=256,d=4,p=(641,1153)` (or equally precise source-comparable target) and checking **one decisive code-distance witness/rank gate only**. Do **not** retry sign-diagonal/tensor Hadamard variations or start a different topic autonomously. If no decision, stop.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/OPEN_RESEARCH_BRANCHES.md` — long-term index.
3. `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md` — I153 exact witness and scope.
4. `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md` — I152 single-flip obstruction.
5. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md` — original RS prime-root mismatch.
6. `findings/vfhe-crt-lookup-cross-component-soundness.md`; `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — I59–60 parent issue.
7. Other earlier failures only when needed; `logs/state-pre-session-handoff-2026-10-13-iteration151.md` stores pre-handoff history.

## STATUS

**I153 CLOSED: FAIL quadratic/tensor-sign Hadamard source-comparable code distance / PASS beta2 toy signed no-wrap and exact low-weight witness / P1 vFHE CRT scalar consistency OPEN-HUMAN_REVIEW / NO ACTIVE ITERATION / I154 NOT STARTED / HUMAN PI DECISION REQUIRED.**

No outreach or public vulnerability disclosure; no verified latest-official-source exploit or published contribution. Read-before-write, one primary hypothesis plus one minimal decisive test per PI-authorized iteration.
