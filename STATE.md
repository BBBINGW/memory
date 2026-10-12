# STATE.md — FHE Research Agent

Last completed: **Iteration 115 (2026-10-12)**.
Active paper: Li et al., *Leveled Functional Bootstrapping via External Product Tree*, ePrint **2025/022**. Public 35-page full PDF: https://eprint.iacr.org/2025/022.pdf. Research MCP metadata retrieval blocked by leading-zero ID normalization; the PDF was read through public web text. PDF screenshot retrieval failed, so independently visually verifying exact subscripts remains pending.

## Active result: I115
[FACT] In paper §4.2, physical pp16–17, PRCA Algorithm5 merges ciphertexts ct_(2j),ct_(2j+1) using shifts X^(N/2^i) and automorphisms X→X^(2^i+1), then prints trace from K_N to K_(N/B) and multiplication by temp=1+...+X^(N/B−1). The claimed ordered packing is Σ m_j X^(jN/B) temp.
[DERIVATION] Under the natural input order, the noiseless tree places m_j at exponent bitrev_(log2 B)(j)*N/B instead. Also, when B²>N, the printed trace to K_(N/B) does not contain every required X^(jN/B) term. The paper's own log2(N/B) trace-operation count is instead consistent with a trace to K_B. This may be an indexing convention/subscript oversight rather than an implementation problem.
[ONE EXACT TEST] Fraction-based negacyclic simulation of all B one-hot inputs: N16/B4 2/4 outputs correctly ordered; N16/B8 1/8; N32/B4 2/4; N32/B8 2/8; N1024/B16 4/16. Reordering inputs by public bit reversal and tracing to K_B gives B/B correct in every case. N16/B4 input (0,1,0,0) yields X8*temp versus intended X4*temp. N16/B8 input j4 is eliminated by trace K2, whereas K8 preserves it. Linear-basis correctness extends to every vector of constant plaintexts under the exact ideal ring operations.
[STATUS] PASS literal pseudocode contradiction; UNCLEAR whether Algorithm6 LUT encoding or the authors' OpenFHE code already corrects the ordering. No compiled FHE test and no demonstrated algorithmic contribution.
Finding: `findings/lfbs-prca-bit-reversal-and-trace-subring-iteration115.md`.
Reproducer: `/mnt/data/iteration115_lfbs_prca_plaintext_gate.py` SHA256 3280fa597584ed7488151429b7a8e0f9f014a21a920334fe195d6470f002fff6.
JSON: `/mnt/data/iteration115_lfbs_prca_plaintext_gate_results.json` SHA256 d293f4cd3239d246a98643d62ae1ad3ba133f3931ddc8c76d0365852f7f2958d.

## NEXT_ACTION — ONE TEST (I116)
Check paper Algorithm6 indexing and any verifiable author OpenFHE implementation for input bit-reversal / correct K_B trace. If implementation is unavailable, report UNKNOWN implementation impact and park the source-only notation concern; avoid asserting operational correctness failure. One hypothesis and one cheapest decisive test, then update state.

## Research protocol and historical preservation
Human = PI, controls strategy, novelty and outreach. Agent = research student; one smallest falsifiable claim plus one cheapest decisive test per iteration. Read original source, distinguish FACT/DERIVATION/SPECULATION, avoid automatic escalation; no author outreach or public release.
**Full unabridged pre-I115 research state**: `logs/state-pre-iteration115-prca-handoff.md` (exact snapshot of I114 STATE). Do NOT delete or rewrite it. I114 low-novelty PRCA count: `findings/lfbs-prca-variable-B-complexity-scope-iteration114.md`. I112–113 Paiva cross-level key reuse parked; I110–111 sparse-SAB sign parked; I108–109 Carousel rounding parked; I103–107 SIMD-ALU cutoff parked; I99–102 nested-RNS weight-factorization parked; I95–98 PaCo parked; RIG parked; GL generic BigSwitch archived.
**Preserve original vFHE CRT lookup ideal-IOP finding** from ePrint2025/286, separate from archived direct bounded-public-A/Brakedown repair. Prior source state `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`. Not a verified compiled SNARK failure.
