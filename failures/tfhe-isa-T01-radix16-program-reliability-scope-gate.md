# TFHE-ISA T01 — Basis-16 program reliability certificate: paper already flags scope

**2026-10-15 Asia/Tokyo. T01 COMPLETE; T02 NOT STARTED.**
**STATUS:** FAIL proposed novel omission of DFR/radix tradeoff, PASS exact limited source-parameter union-bound calculation; actual fair same-DFR performance & program-wide empirical failure rates UNCLEAR. PARK this low-novelty branch. Separate from PVFHE-P27 PARK and vFHE V42 SOURCE_BLOCKED.

## Read-before-write / source basis
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md 3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c (vFHE V42, NOT EDITED), P27 findings/pvfhe-P27-coeff-bitwidth-wire-provenance-gate.md SHA 633a34d8e667d4941d1986b7d7935fb7d9276389, and OPEN_RESEARCH_BRANCHES.md SHA 28d4811ca5b43830c123d75db98b1eecd2f2a606 to avoid prior LCR+AKS etc. Destination T01 did not exist before write.

**Primary original FULL TEXT ACTUALLY READ:** Daphné Trama, Pierre-Emmanuel Clet, Aymen Boudguiga, Renaud Sirdey, Nicolas Ye, *Designing a General-Purpose 8-bit (T)FHE Processor Abstraction*, TCHES2025 / IACR ePrint 2024/1201, https://eprint.iacr.org/2024/1201; Research MCP full 48 physical pp, cached GitHub mirror SHA256 ebe98ea393e91f814a2a6098809f2c095de0bf4867c4693b8925df4b8a13ea09, VERSION_UNVERIFIED. Read pp6–11,20–23,28–30. This is primary-sourced and NOT an abstract-only literature guess.
Other candidate fresh papers ePrint2026/1163 SWIFT, 2025/261 HasteBoots and 2024/115 BGV null polynomials were attempted but their full Research MCP PDFs were unavailable (403 or identity failure). No source-derived claims about their content beyond their metadata; no fake full-text audits.

## ONE falsifiable hypothesis and decisive test
**[HYPOTHESIS T01]** Paper's B16 fastest-basis optimization overlooks low DFR / whole-program reliability and thus exposes a previously unrecognized optimization boundary.
**[FALSIFIER]** Read paper p29 Conclusion to check whether authors themselves explicitly identify radix-dependent DFR/parameter tradeoff; then exactly compute per-MVB-tree evaluation source Table2 union-bound certificate for one program-level error target. If stated already, novelty dies irrespective of arithmetic.

## Source facts
- Physical pp9–10 §4.2.1 and p10 Table1: under selected ~128-bit TFHE parameter sets, B16 has fastest measured non-bitwise LUTeval/MVLUTeval. The 8-bit output examples are B16 MVLUTeval-star (two 4-bit output digits) **0.23s**, B4 MVLUTeval-diamond (four 2-bit output digits) **1.98s**. This is NOT a matched-DFR, matched-memory, full-program optimization theorem. Source notes bitwise work can favor B4.
- Physical p11 Table2 says **error probability of ONE MVB tree-based evaluation** ε_B4=2^-30, ε_B8=2^-23, ε_B16=2^-23. Different parameter sets and baselines; do not treat ε as the probability of a base BlindRotate/PBS.
- **CRITICAL direct pre-emption, physical p29 Conclusion:** source explicitly recognizes baseline bootstrapping error probability around **2^-40**, says newer 2^-128 bootstrapping DFR parameters available only at B2, that achieving B16 with such low failure is challenging, and B4 **might be optimal in that regime**. The source itself acknowledges exactly the tradeoff hypothesized to be omitted. Its 2^-40 baseline bootstrapping metric is NOT identical to Table2's per-MVB 2^-23 metric; do not call it a contradiction.

## Minimal exact model and independent executed test
For m source-defined MVB tree evaluations and ε_B per-event upper bound, union bound independent of any error correlation:
    Pr[at least one error] <= min(1,m ε_B).
For illustrative program failure-budget δ=2^-20 NOT claimed as an original-paper requirement, the maximal m whose error can be CERTIFIED solely from Table2 is
    B4: floor(δ/2^-30)=1024;
    B8: floor(δ/2^-23)=8;
    B16: floor(δ/2^-23)=8.
For **m=256** such individual evaluations, B4 gives ≤2^-22 and B8/B16 ≤2^-15, so B4's published upper bound SUFFICES for δ while B16's published bound does NOT. This is not proof that B16 actually fails or that a B4 8-bit application is more efficient; counts of tree evaluations per 8-bit program and error correlations remain unspecified. Unlike directly comparing Table1, using m avoids conflating four 2-bit output ciphertexts with two 4-bit ciphertexts. The union bound is conservative and not a measured DFR.

ACTUALLY EXECUTED exact integer/Fraction script:
- /mnt/data/tfhe_isa_T01_program_reliability_gate.py SHA256 8c887522f2424f6f88c89ee2c84d9ab5a83b766d646c34f8e4fc65e7d70bcce2
- /mnt/data/tfhe_isa_T01_program_reliability_results.json SHA256 8e7bca52a80730090e99a04ef072d27830c712b2f9d090ed32bd1364fcf6899e
- Full markdown report /mnt/data/TFHE_ISA_T01_Radix_Reliability_Certification_Gate.md SHA256 4263f187ebc53a53bc8149ef565b135d77745f13f65b0cb0d4882c5836ffc475.
No full TFHE evaluation, empirically observed failure, security-parameter reoptimization, hardware rerun or QROM proof.

## End of iteration
**STATUS:** FAIL claimed overlooked DFR/radix research gap because paper explicitly acknowledges it; PASS source-derived exact certification frontier; overall novel improvement, real DFR/security and fair latency UNCLEAR.
**RESULT:** In source's measured parameter regime B16 faster for representative LUTs but uses per-MVB failure upper 2^-23 vs B4 2^-30. A conservative program-wide union bound materially constrains the number of covered evaluations. HOWEVER paper p29 already acknowledges that lower-DPF targets can make B4 preferable, so no new paper flaw or contribution emerged.
**NEXT_ACTION:** PARK TFHE-ISA-T01. Only pursue this theme with a genuinely NEW mechanism (matched-global-DFR radix-parameter cooptimization, rigorous correlated failure bound, or fair benchmark) and a distinct falsifiable claim; otherwise pivot to another primary-original-accessible FHE problem. Do NOT resume PVFHE-P27 or vFHE V42 without missing official compiler/PDF evidence.
**STATE_UPDATE:** YES one standalone failure archive ONLY; no changes to global STATE.md, independent PVFHE/P-series, vFHE/SHIP or OPEN_RESEARCH_BRANCHES.md.