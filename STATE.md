# FHE Research State — After Iteration 154

**Checkpoint:** 2026-10-13 · `main` · I154 completed, I155 **NOT STARTED**.
**Authority:** This file is a compact recovery entry point, not a history log. The former full 84,552-character `STATE.md` is preserved verbatim at `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`). Long-term directions and archives are indexed in `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI makes direction, continuation, novelty and disclosure decisions.

## CURRENT TARGET

**Research direction (OPEN/HUMAN_REVIEW; no ACTIVE experiment):** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, **IACR ePrint 2025/286**. Audit/possible low-cost repair for **global diagonal integer scalar-digit lookup across CRT field components** in §4.3 Theorem 4.8 / §5 Brakedown PCS. Primary full 52-physical-page PDF was read through Research MCP from a GitHub mirror (PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`); equality to the latest official revised ePrint PDF remains **VERSION_UNVERIFIED**. Relevant source: §3.1, §4.3 physical pp20–23, §5 pp25–26, Appendix F.2/F.3 physical pp50–52. Original author public code: `vfhe/proof-friendly-CKKS`.

## LAST COMPLETED ITERATION

**154 (2026-10-13)**; **I155 NOT STARTED**. PI's “好的，请继续” following I153 was narrowly interpreted as permission for ONE new non-Hadamard, non-tensor candidate test under the same P1 target. Cyclic-window systematic integer encoder FAILS source-comparable distance by adjacent-message cancellation. Latest archive below.

## CURRENT QUESTION

Original P1: can a field-independent bounded-integer, fast code make already authenticated Brakedown F.2 **testing-phase Merkle columns** check global cross-CRT scalar-digit coherence without new costly MLE evaluation openings, **while preserving original F.3 code distance and security**? Three explicit integer-encoder families (I152–154) fail distance; parent vFHE global CRT scalar-digit soundness issue remains **OPEN/HUMAN_REVIEW**; **no active coding candidate**.

## PRIMARY HYPOTHESIS

**NONE ACTIVE**. I154 [NEGATIVE/FAIL]: `E_{m,L}(x)=(x,f_L x mod(X^m-1))`, `f_L=1+X+…+X^(L-1)`, `m=N=256,d=4,L=64,p=(641,1153), beta=2`, is a field-independent integer `[512,256]` systematic cyclic-window code with **O(m)** encoding and honest integer centered no-wrap (`64<641/2`). A singleton has weight65, but adversarial field message `x=1-X` produces codeword `(1-X,1-X^64)` of **weight4** in both primes, while source Appendix F.3 direct-sum RS `4×[128,64,65]` has exact dmin65. All `1≤L<m` have `dmin≤4`; relative `≤2/m→0`. Detailed evidence: `failures/vfhe-cyclic-window-integer-encoder-local-cancellation-iteration154.md` (SHA `081e681429f059361218716512ac6b3ef00c4f3c`).

## CURRENT EVIDENCE

- **[DERIVED/EXACT I154; NEGATIVE]** Source-compatible `m=N=256,d=4,p=(641,1153)`. Sliding-window integer code with 64-term parity windows has common integer honest values and `O(m)` encoding; however `(1-X) f_L=1-X^L` makes a weight4 codeword, vs F.3 RS exact distance65. Universal `δ≤2/m`; this is local cancellation and independent of the prior Hadamard obstructions. Archive `failures/vfhe-cyclic-window-integer-encoder-local-cancellation-iteration154.md`.
- **[DERIVED I153; NEGATIVE]** Multi-flip/tensor Hadamard has `dmin≤2√m`, `δ≤1/√m`, and at m256 exact witness weight32 < RS65. `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md`.
- **[DERIVED I152; NEGATIVE]** One-coordinate-sign-flip Hadamard exact `dmin4` all m power-of-two ≥4. `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md`.
- **[DERIVED I151; NEGATIVE]** Original per-prime native RS code columns cannot be compared as common bounded integers even on honest inputs: toy source-root j1 values 12 vs 6. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`.
- **[DERIVED I59–60; HUMAN_REVIEW]** Ideal PIOP-level and abstract composition CRT *diagonal scalar-digit* issue; not a verified latest-official-version defect or compiled end-to-end SNARK forgery. `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`.
- **[FACT]** Original paper ePrint 2025/286 §3.1, §4.3, §5, Appendix F.2/F.3 (physical pp51–52 latest re-read): F.2 uses Merkle-authenticated row-encoded columns; F.3 uses native-field RS `[N/2,N/4,N/4+1]`. Full 52-page PDF from GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** against official most recent revision. Formula extraction warning. Author NTT benchmark `vfhe/proof-friendly-CKKS/lib/main_benchmark.cpp` SHA `f92e054ae758ddf3c35e22d1a0294374ef2d6b3e`.
- **[PARKED]** I95 expensive direct Brakedown, I136–138 PCS micro-batching, I148 masks small gain, I149/150 one-point integer lifts blocked. See `findings/OPEN_RESEARCH_BRANCHES.md`. Previously reported strict `p<2^49` is a conditional simplification (some source primes exceed).

## MAIN OBSTRUCTION

Original F.3 RS is field-dependent, preventing direct honest CRT integer comparison (I151). Three **different fast field-independent integer encoders** all have low-weight codewords despite toy no-wrap and favorable nominal encoding complexity: I152 rank-one Hadamard flip, I153 tensor Hadamard, I154 overlapping cyclic sliding window. None maintains native-field RS distance at a source-compatible instance. No efficient secure CRT scalar-index binding/PCS repair exists. Do not keep generating nearby coding variants without a new coding-theory architecture with a credible source-comparable distance guarantee.

## OPEN UNCERTAINTY

**[OPEN]** Existence and novelty of a genuinely nonlocal bounded-integer ECC with source-comparable distance and near-linear encoding over each native extension field, no-wrap for actual digit limits, and secure reuse of the source's Brakedown testing columns. Also Fiat–Shamir/PCS binding, key/privacy, 128-bit communication/verifier cost, actual compiled impact of I59–60, and current official ePrint binary equality are NOT verified.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**HUMAN_REVIEW / PI DECISION REQUIRED; I155 NOT STARTED.** Choose ONE: **(a)** park the concrete integer-encoder/Brakedown testing-column repair line (retain parent P1 ideal CRT issue OPEN) pending a materially different theoretical premise or coding-theory prior art; **(b)** expressly nominate/authorize a genuinely new high-distance nonlocal integer ECC family with an explicit credible construction and one source-comparable **minimum-distance gate** before any PCS work; **(c)** direct a separate PI-authorized review of source-version/impact rather than keep proposing fast encoder variants. Do not silently restart archived variants or pivot to another FHE target. No outreach/disclosure without PI authorization.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/OPEN_RESEARCH_BRANCHES.md` — durable other-direction index; current `STATE.md` overrides iteration/NEXT_ACTION.
3. `failures/vfhe-cyclic-window-integer-encoder-local-cancellation-iteration154.md` — I154 new local-cancellation failure.
4. `failures/vfhe-quadratic-tensor-hadamard-crt-encoder-distance-iteration153.md` and `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md` — earlier structural code-distance failures.
5. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md` — original native RS honest mismatch.
6. `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — P1 parent issue.
7. Other archived failures only if directly relevant; `logs/state-pre-session-handoff-2026-10-13-iteration151.md` for old history only.

## STATUS

**I154 CLOSED: FAIL cyclic-window source-comparable native-field code-distance criterion / PASS honest beta2 no-wrap and exact adjacent-cancellation counterexample / P1 vFHE CRT scalar consistency OPEN-HUMAN_REVIEW / NO ACTIVE EXPERIMENT / I155 NOT STARTED / HUMAN PI DECISION REQUIRED.**

No public vulnerability assertion, no outreach or disclosure. Primary source remains VERSION_UNVERIFIED, no end-to-end SNARK proof attack, and no positive verified encoding construction.
