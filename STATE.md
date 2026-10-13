# FHE Research State — After Iteration 152

**Checkpoint:** 2026-10-13 · `main` · I152 completed, I153 **NOT STARTED**.
**Authority:** This file is a compact recovery entry point, not a history log. The former full 84,552-character `STATE.md` is preserved verbatim at `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`). Long-term directions and archives are indexed in `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI makes direction, continuation, novelty and disclosure decisions.

## CURRENT TARGET

**Research direction (OPEN/HUMAN_REVIEW; no ACTIVE experiment):** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, **IACR ePrint 2025/286**. Audit/possible low-cost repair for **global diagonal integer scalar-digit lookup across CRT field components** in §4.3 Theorem 4.8 / §5 Brakedown PCS. Primary full 52-physical-page PDF was read through Research MCP from a GitHub mirror (PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`); equality to the latest official revised ePrint PDF remains **VERSION_UNVERIFIED**. Relevant source: §3.1, §4.3 physical pp20–23, §5 pp25–26, Appendix F.2/F.3 physical pp50–52. Original author public code: `vfhe/proof-friendly-CKKS`.

## LAST COMPLETED ITERATION

**152 (2026-10-13)**. **I153 NOT STARTED.** I152 was explicitly requested after handoff; toy distance/no-wrap PASS, but the same single-flip Hadamard family has vanishing relative distance and is rejected as a scalable Brakedown replacement.

## CURRENT QUESTION

Can some *different* field-independent, bounded-integer, fast linear encoder make already-authenticated Brakedown **testing-phase Merkle columns** verify cross-CRT scalar-digit coherence without costly additional native MLE evaluation openings, *while retaining source-comparable code distance and soundness*? The concrete I152 single-coordinate-sign-flip Walsh–Hadamard encoder has been falsified as a scalable high-distance candidate. Parent P1 vFHE issue remains OPEN/HUMAN_REVIEW; **no new candidate has been authorized or selected**.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I152 [NEGATIVE/FAIL candidate at scale, TOY PASS]: for `Enc_Z(x)=(H_m x,H_m D x)` with only the final input sign flipped, the prescribed `m=4,p=29,37` rank test gives `[8,4,d_min=4]` and beta2 honest no-wrap `4<29`. However for **every power-of-two m>=4** over odd-characteristic fields, `d_min=4` exactly and relative distance `2/m` tends to zero. See `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md`. No ACTIVE I153 experiment. PI must decide whether to propose/authorize a *different* candidate or park this branch.

## CURRENT EVIDENCE

- **[DERIVED/EXACT I152; NEGATIVE scalable encoder]** Rank tests over F29/F37: maximum four zero output coordinates, dmin4; beta2 integer coefficient sum ≤4<29. Algebraically for all m=2^k≥4, `T=H_m D H_m^{-1}=I-(2/m)uu^T`; choosing 2-sparse y with `u^Ty=0` makes codeword `(y,y)` weight4, and the involution gives lower bound4. Thus relative distance exactly 2/m, not a source-comparable high-distance family. Archived and reread at `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md` (blob SHA `1191c8313e0b540f4f70722b3c78575749e93b6b`). This is not an attack on original vFHE or a complete PCS repair.
- **[FACT]** Original Appendix F.2 commits row-encoded matrices as Merkle column leaves; testing phase opens columns, whereas evaluation phase sends separate vectors. F.3 uses native-field Reed–Solomon `[N/2,N/4]` encodings evaluated at **per-prime roots of unity**. Author `vfhe/proof-friendly-CKKS/lib/main_benchmark.cpp` SHA `f92e054ae758ddf3c35e22d1a0294374ef2d6b3e` implements RS encoding as zero-padded coefficient NTT.
- **[DERIVED, I151 PASS exact counterexample]** Source-form toy `N=8,d=4,p0=29,p1=37` with fourth roots `12` and `6`: common **honest** scalar message `x=(0,1)` corresponds to `f(Z)=Z`, but the two codewords are `(1,12,28,17)` and `(1,6,36,31)`. Same code-column index 1 gives **12 vs 6**. Hence naïve cross-prime small-integer comparison of existing F.3 RS-coded leaves **fails honest completeness**. Details/reproduction and boundaries in `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`, SHA `52d8d71bc8e4c2a4548fa2919c33b1c8213596a0`.
- **[DERIVED, older I59–60; HUMAN_REVIEW]** Componentwise CRT-field membership does not by itself certify **one common diagonal scalar digit**. There is an **ideal PIOP-level** counterexample and composition audit in `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`. **Not a compiled end-to-end SNARK attack or verified defect of a latest official revision.**
- **[NEGATIVE/PARKED]** I95 bounded-public-integer/direct Brakedown fix was too expensive; I136–138 native PCS 4→1 shortcuts failed; I148 bounded-alphabet rank-one masks gave only local arithmetic gains; I149 small-single-prime MLE lift failed honest completeness; I150 full-`Q` **single-point** integer lift did not provide negligible detection. See Backlog and files below.
- **[SOURCE CAUTION]** Author's benchmark contains primes slightly **greater** than `2^49`; old I149–150 statements using strict `p<2^49` are *conditional size approximations*, not a literal guarantee for every implementation parameter.

## MAIN OBSTRUCTION

Existing native RS encoding is field-dependent, obstructing honest cross-prime integer comparison of source testing columns (I151). A new shared integer encoder must simultaneously guarantee (i) sufficient Hamming distance in every original F_(p_i^d), (ii) exact common small integers/no-wrap, (iii) fast encoding and (iv) valid original F.2 testing/commitment binding and soundness. **I152 shows a single-coordinate-flip Hadamard pair cannot meet the scalable distance condition**: rate 1/2 but minimum relative distance 2/m. No viable alternative or full security/cost result is established.

## OPEN UNCERTAINTY

**[OPEN]** Existence of a different fast, bounded, field-independent encoder with source-comparable minimum distance, safe integer outputs at *actual* digit bounds, and efficient secure global CRT consistency proof. Also original Fiat–Shamir/PCS privacy and full 128-bit cost/security consequences, latest official PDF version, and end-to-end impact of I59–60 remain unverified. I152's single-flip family is **closed**, not awaiting additional parameter sweeps.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**HUMAN PI DECISION REQUIRED; I153 NOT STARTED.** Choose **one** of: (a) keep P1 vFHE active for another minimal falsifiable test **only after supplying or explicitly authorizing a genuinely different concrete field-independent bounded-integer fast encoder candidate**, with *distance* as the first gate; or (b) park this repair path. Do not retry I152's single-flip Walsh–Hadamard family, revive other archived failures, or choose a different target on the agent's own initiative. If (a), first predeclare exact candidate, source-comparable distance target, field/ring regime and cheapest rank/structural test.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/OPEN_RESEARCH_BRANCHES.md` — durable branch index and status.
3. `failures/vfhe-single-flip-hadamard-crt-integer-encoder-distance-iteration152.md` — latest encoder test, exact ranks, no-wrap, universal distance obstruction and limits.
4. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md` — native F.3 RS column failure.
5. `findings/vfhe-crt-lookup-cross-component-soundness.md`; `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — I59–60 parent issue.
6. Consult `failures/vfhe-full-crt-q-short-lift-small-integer-challenge-soundness-iteration150.md`; `failures/vfhe-small-integer-mle-point-opening-crt-lift-iteration149.md`; `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` **only as needed**.
7. `logs/state-pre-session-handoff-2026-10-13-iteration151.md` — prior long historical state snapshot, only if older details absent from current archives.

## STATUS

**I152 CLOSED: FAIL single-flip Hadamard scalable code-distance candidate / PASS prescribed [8,4] rank and beta2 no-wrap toy gate / P1 vFHE CRT scalar consistency OPEN-HUMAN_REVIEW / NO ACTIVE ITERATION / I153 NOT STARTED / HUMAN PI DECISION REQUIRED.**

No outreach or public vulnerability disclosure; no official-source exploit or published contribution claim. Read-before-write, one smallest hypothesis and one cheapest decisive test per PI-authorized iteration.
