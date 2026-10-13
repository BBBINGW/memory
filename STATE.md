# FHE Research State — Session Handoff After Iteration 151

**Checkpoint:** 2026-10-13 · `main` · I151 completed, I152 **NOT STARTED**.
**Authority:** This file is a compact recovery entry point, not a history log. The former full 84,552-character `STATE.md` is preserved verbatim at `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`). Long-term directions and archives are indexed in `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI makes direction, continuation, novelty and disclosure decisions.

## CURRENT TARGET

**Research direction (OPEN/HUMAN_REVIEW; no ACTIVE experiment):** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, **IACR ePrint 2025/286**. Audit/possible low-cost repair for **global diagonal integer scalar-digit lookup across CRT field components** in §4.3 Theorem 4.8 / §5 Brakedown PCS. Primary full 52-physical-page PDF was read through Research MCP from a GitHub mirror (PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`); equality to the latest official revised ePrint PDF remains **VERSION_UNVERIFIED**. Relevant source: §3.1, §4.3 physical pp20–23, §5 pp25–26, Appendix F.2/F.3 physical pp50–52. Original author public code: `vfhe/proof-friendly-CKKS`.

## LAST COMPLETED ITERATION

**151 (2026-10-13)**. **I152 NOT STARTED.** Handoff is administrative, not a new research iteration.

## CURRENT QUESTION

Can a **new field-independent bounded-integer linear encoder** allow the Merkle columns already authenticated in Brakedown's **testing phase** to verify cross-CRT scalar-digit coherence, **without extra costly native MLE evaluation-phase openings**, while maintaining native-field code distance, no-wrap, fast encoding and proof binding? The architecture is an **unverified opportunity**, not a working repair.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** Latest tested I151 claim **[NEGATIVE/FAIL]**: identical honest integer digit rows should yield identical small canonical integer RS code-symbols at the same Merkle column across different CRT primes under the original unchanged F.3 encoding. **False**, because the evaluation roots depend on each prime. Candidate for **I152 only upon new PI authorization**: `Enc_Z(x)=(H_m x, H_m D x)`, with Walsh–Hadamard `H_m` and a fixed integer diagonal sign matrix `D`; its minimum distance and native-field behavior are **[HYPOTHESIS]/UNTESTED**.

## CURRENT EVIDENCE

- **[FACT]** Original Appendix F.2 commits row-encoded matrices as Merkle column leaves; testing phase opens columns, whereas evaluation phase sends separate vectors. F.3 uses native-field Reed–Solomon `[N/2,N/4]` encodings evaluated at **per-prime roots of unity**. Author `vfhe/proof-friendly-CKKS/lib/main_benchmark.cpp` SHA `f92e054ae758ddf3c35e22d1a0294374ef2d6b3e` implements RS encoding as zero-padded coefficient NTT.
- **[DERIVED, I151 PASS exact counterexample]** Source-form toy `N=8,d=4,p0=29,p1=37` with fourth roots `12` and `6`: common **honest** scalar message `x=(0,1)` corresponds to `f(Z)=Z`, but the two codewords are `(1,12,28,17)` and `(1,6,36,31)`. Same code-column index 1 gives **12 vs 6**. Hence naïve cross-prime small-integer comparison of existing F.3 RS-coded leaves **fails honest completeness**. Details/reproduction and boundaries in `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`, SHA `52d8d71bc8e4c2a4548fa2919c33b1c8213596a0`.
- **[DERIVED, older I59–60; HUMAN_REVIEW]** Componentwise CRT-field membership does not by itself certify **one common diagonal scalar digit**. There is an **ideal PIOP-level** counterexample and composition audit in `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`. **Not a compiled end-to-end SNARK attack or verified defect of a latest official revision.**
- **[NEGATIVE/PARKED]** I95 bounded-public-integer/direct Brakedown fix was too expensive; I136–138 native PCS 4→1 shortcuts failed; I148 bounded-alphabet rank-one masks gave only local arithmetic gains; I149 small-single-prime MLE lift failed honest completeness; I150 full-`Q` **single-point** integer lift did not provide negligible detection. See Backlog and files below.
- **[SOURCE CAUTION]** Author's benchmark contains primes slightly **greater** than `2^49`; old I149–150 statements using strict `p<2^49` are *conditional size approximations*, not a literal guarantee for every implementation parameter.

## MAIN OBSTRUCTION

The original RS generator is **field-dependent**, so authenticated codewords of identical honest scalar inputs need not have a common integer interpretation. A replacement encoder must achieve (i) sufficient relative Hamming distance over each original `F_(p_i^d)`, (ii) exact common integer outputs without modular wrap, (iii) near-linear or source-comparable encoding cost, and (iv) secure integration into original Brakedown testing/binding and global CRT digit relation. **No such replacement or full proof has been established.**

## OPEN UNCERTAINTY

**[OPEN]** Candidate `(H_mx,H_mDx)` minimum distance, code rate/no-wrap against actual parameters, codeword sampling/commitment security, number of extra Merkle openings, actual communication and verifier cost, Fiat–Shamir/VC privacy, novelty. Also unverified latest official PDF and compiled end-to-end security impact of I59–60. Other branches are **PARKED or SOURCE-BLOCKED**, not deleted; see `findings/OPEN_RESEARCH_BRANCHES.md` (MRFHE, AR24, SPRU, FAB, TFHE and others).

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**Only if human PI explicitly authorizes I152:** Test ONE candidate integer-coefficient encoder, `Enc_Z(x)=(H_4x,H_4Dx)`, with standard 4×4 Walsh–Hadamard `H_4`, fixed `D=diag(1,1,1,-1)`, over the same small odd source-form fields `F29` and `F37`. **Before any new PCS design**, compute the **exact [8,4] linear-code minimum Hamming distance** via generator-matrix subset-rank tests and compare with a predeclared illustrative target `d_min≥2` (relative distance ≥1/4). Also record the toy **honest no-wrap precondition** at `β=2`: column absolute sum ≤4 and digit bound ≤1, so upper magnitude ≤4<29. Any dmin<2 or other structural distance obstruction kills this candidate at the toy gate. **PASS of this tiny test would NOT certify large-parameter distance, cost, security or contribution.** Do not execute I152 until authorized; do not choose a different target autonomously.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/OPEN_RESEARCH_BRANCHES.md` — durable branch index and status.
3. `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md` — latest primary hypothesis, source, exact minimal counterexample and limits.
4. `findings/vfhe-crt-lookup-cross-component-soundness.md`; `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — I59–60 parent issue.
5. Consult `failures/vfhe-full-crt-q-short-lift-small-integer-challenge-soundness-iteration150.md`; `failures/vfhe-small-integer-mle-point-opening-crt-lift-iteration149.md`; `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` **only as needed** to avoid repeating known failures.
6. `logs/state-pre-session-handoff-2026-10-13-iteration151.md` — **verbatim pre-handoff 84 KB STATE snapshot**, only for older details missing from primary findings/failures; not mandatory for ordinary startup.

## STATUS

**SESSION_HANDOFF_COMPLETE / I151 CLOSED: FAIL existing F.3 RS column CRT canonical-integer equality, PASS exact honest counterexample / P1 CRT scalar consistency OPEN-HUMAN_REVIEW / NEW INTEGER ENCODER UNTESTED / NO ACTIVE ITERATION / I152 NOT STARTED.**

No outreach or public vulnerability disclosure; do not imply official-source exploit or published contribution. Read-before-write, one smallest hypothesis plus one cheapest decisive test per PI-authorized iteration.
