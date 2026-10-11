# Iteration 73 — Source-grounded Pi_AC GKR Eq(16)–(20) wire/oracle consistency audit for the bounded-output vFHE CRT range counterexample

Date: 2026-10-11
Paper: Ignacio Cascudo, Anamaria Costache, Daniele Cozzo, Dario Fiore, Antonio Guimarães, Eduardo Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO 2025), IACR ePrint 2025/286.
Primary STATUS: **PASS** (all displayed §4.2 Eq16–20, Appendix E.1 source-defined wiring conditions can be fulfilled by one consistent D1 W1 false-computation trace; nontrivial honest sumchecks for Eq16 and Eq20 and local zero-equation transcripts for 17–19 verified).
QUALIFICATION: **UNCLEAR** for every message of the authors' exact optimized Pi_AC variable-packing schedule and complete compiled/Fiat–Shamir SNARK; script uses algebraically faithful padded-index virtual-oracle reductions, with Eq20's aux and out sums bundled into a 3-variable oracle (not exactly paper's encoding). Proof of formal source algebraic relations is stronger than merely evaluating Eq13, but is NOT a serialized attack proof.
No authors contacted, no publication or issue, no modifications to unrelated parked RIG-HE STATE.md.

## Read-before-write and primary falsifiable hypothesis
Read AGENT.md, RESEARCH_PHILOSOPHY.md, unrelated RIG-HE STATE.md, and I72 finding `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`. Source Research MCP 52pp revised-looking mirror ePrint PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, Git blob `a549654c5dffa3484e95e8244056f4a27c48c3e6`; mirror pinned April 28, 2026, version_status VERSION_UNVERIFIED vs current official PDF SHA.
[PRIMARY HYPOTHESIS — PASS at source algebra level] Appendix E.1 Π_AC explicit GKR consistency checks (Eq16–20) impose an additional quotient-to-remainder or public-output-binding constraint that will PREVENT I72's false zero-input / public y=173 rescaling witness, even though Eq11/13 and CRT-rectangular lookup pass.
[FALSIFIER] Build an explicit fixed-witness assignment to all V0–V3 wire groups and show Eq16–20 hold as multilinear/predicate identities; demonstrate honest local sumcheck transcripts including the nontrivial Eq16 and Eq20 oracle relations. The required claim (that PiAC adds a fatal check) is falsified if all pass. Cheapest test = read §4.2 pp16–20 and Appendix E.1 pp44–46 and run ONE exact D1 W1 3-prime source-indexed checker; avoid more parameter variants.
[RESULT] All displayed equations pass. PiAC does not restore the lost scalar-digit consistency. An additional *unexpected stronger* quotient/remainder check was found in Eq16, explicitly included in this verification; its exact arithmetic is met by I72's witness.

## Source locations read this iteration
[FACT] §2.2 pp7–9 Def 2.3/2.4: indexed oracle statements can contain public polynomial pointers and witnesses; verifier queries random evaluations. An honestly consistent public-output oracle is not an independent semantic CKKS Eval check.
[FACT] §4.1 p13–15: Eq11 base-decomp consistency, Eq13 rescale arithmetic, explicit R_CKKS=C(x,w_2^u,{w_l},y)=0 and bounded ranges. `Jy~` output oracle, `Jw~_{2^u}` all auxiliary key-switch/decomp/remainders; D1 has no intermediate quotient oracle. Footnote 7: y range check can be removed when y is known to verifier, so we instead require y to satisfy TRUE bound directly.
[FACT] §4.2 p17 Eq16: V0 is zero check layer, rescon_1 selects c'_b, rescon_3 adds **−1 times remainder** and **−p_l times quotient**; bdcon adds d2 minus fixed CRT recomposition weights times base-decomp inputs. Thus the key rescale check is **c'_b−w_rmd,b−p_l*w_quot,b=0 modq**, NOT just a check using a multiplicative inverse coefficient in Eq13. This was the crucial extra condition to audit.
[FACT] §4.2 p18 Eq17 relates c'_b to d_b and evk weighted BD; Eq18 relates pre-multiply d values to input and prior-layer quotients (for D1 no prior layer); p18–19 Eq19 maps subsets d01,d2 to full V2 oracle by index selectors.
[FACT] §4.2 p19 Eq20 and Appendix E.1 pp44–45 Eq30, Π_AC steps 1–6: routing of V3 quotient, BD and IP wires to public V_out and auxiliary V_aux by selector predicates C_o and C_a, with four random linear combination coefficients; final verifier opens public input, public output and auxiliary oracle evaluations.
[FACT] Appendix E.1 p45 Theorem E.1 invokes completeness of sum-check; D.3 p43–44 replaces oracle queries with PC openings and preserves relation only if original PIOP relation is sound; no independent arithmetic re-evaluation of CKKS semantics is added at that compilation description.
[ATTENTION] Some pdf text extraction of Eq13 brackets is ambiguous. Eq16's predicate coefficients −1 and −p_l are legible and yield a completely independent stronger necessary relation; no reliance on ambiguous Eq13 parentheses.

## Fixed single witness — exact quotient equation
N8 d4 D1 W1, prime list [149,157,173], q=4,046,989, dropped prime p_l=173, surviving q'=23393. All source §3.1 p_i=4a+1 with odd a, each X8+1 splits into two irreducible quartics (I72).
Inputs: two ciphertexts each (0,0); public output y=(173,0) with true coefficient bound y0=173<23393 and y0 mod173=0; true deterministic Eval zero×zero rescale output=(0,0).
Three wks decomposition wires = 0; pre-multiplication d0=d1=d2=0; key-switch outputs c'_0=c'_1=0. Secret evk numeric values irrelevant since multiplied by zero.
Malicious remainder r=(4017060,0). It lies OUTSIDE true rounded coefficient bound [0,256) and actual bound [0,173); but its CRT component-wise digits pass I72's explicit 128-position, base-16 table memory transcripts with beta=16, ell*=7, pmin=149.
**Eq16 stronger ring equation**:
  c'_0−r0−173*y0=0−4017060−29929=−4046989=−q≡0 modq.
  c'_1−r1−173*y1=0.
  d2−Σ_i PW_ω(1)[i]wks_i=0.
Also Eq13 holds with inverse p_l^{-1} mod q_survive=17849; `(−4017060*17849) mod4046989=173`; no inconsistency between original Eq13 and the stronger Eq16 in this specific witness.
Hence all four V0 padded constraint rows are exactly zero, not just with high probability. The small toy ring is not an actual security-parameter instantiation; output range is genuinely legal, independent of range PIOP.

## Exact source-aligned wire assignment
- V3_in=[0,0,0,0] (two input ciphertexts).
- V3_BD=[0,0,0,0] (three BD values zero, one padding).
- V3_quot=[173,0] (internal quotient **identical to public output**).
- V3_IP=[0,0,0,4017060,0,173,0,0], where indices0..2 are BD, 3..4 remainders, 5..6 quotient, index7 zero padding.
- V3_aux,2u (public/committed witness oracle)=[0,0,0,4017060,0,0,0,0] (3 BD,2 remainder,3 zero pads).
- Vout (publicly committed output oracle)=[173,0].
- V2_pre=[0,0,0,0] corresponds d0,d1,d2 plus pad; V1_cprime=[0,0]; V0 residual=[0,0,0,0] corresponds 2 rescon+1 bdcon+pad.
- PW weights are the genuine CRT idempotents [q/pi*(q/pi)^(-1) modpi modq] and sum to 1 modq; all wks=0 so Eq16 BD check true regardless.
- Eq17: cprime= d0/d1 + evk·BD = zero; true for any legitimate evaluation key.
- Eq18: first premultiplication layer has only zero public inputs, hence d0,d1,d2 all zero. There are no nonzero previous-layer quotient multiplications in depth D1.
- Eq19 subset-to-full maps [d0,d1] and [d2] to V2, all zero.
- Eq20 uses the source selector predicates: BD indices (0..2) ↦ aux (0..2), IP indices (0..4) ↦ aux (0..4), IP indices (5,6) ↦ output(0,1), quotient indices(0,1) ↦ output(0,1). All source/destination values match EXACTLY, and any padded indices are zero. Therefore the Eq20 identity holds for arbitrary verifier evaluation challenges and arbitrary linear-combination scalars, not merely sample points.
- Once each displayed gate and mapping is an actual ring identity of MLE tables and wiring predicates, honest corresponding GKR/sumcheck messages exist for every verifier challenge; independent local sumchecks additionally constructed below. The full optimized schedule remains to be verified.

## Reproducible proof audit and transcript limits
Exact Python executed:
 `/mnt/data/iteration73_vfhe_pi_ac_gkr_wiring_audit.py` SHA256 `ade755d160cf10773c4e99f8fc6bd15bc6c2f38742e6578b5859460f2b8ceb6d`.
 `/mnt/data/iteration73_vfhe_pi_ac_gkr_wiring_results.json` SHA256 `c5589c3c9493605dae3a29314bd39c8d24630de8e439c48091d5565980c502bb`.
[EXECUTED] Eq16 residual rows [0,0,0,0], each source-defined polynomial reconstruction at 32 independent r0 challenges zero. Eq17/18/19 all-zero layer identities checked; mapped MLE/source consistency checked on 24*3 independent ring points. Eq20 checked on 32 independently sampled sets of r_quot,r'_quot,r_BD,r_IP and four random aggregation coefficients, with all 32 LEFT and RIGHT nonzero and equal.
[HONEST LOCAL SUMCHECK RECORDS] Exact ring arithmetic, generic standard degree≤2 sumcheck generated with explicit polynomial coefficients and random verifier challenges for Eq16 (3 variables), Eq17 (2 variables, all-zero), Eq18 (2 variables, all-zero), Eq19 (2 variables, all-zero) and Eq20 (3 variables). At each round verified `g_j(0)+g_j(1)=previous_claim`; at the end `g_last(r_last)=oracle_p(r)`. The Eq16 and Eq20 summands are nonzero, proving these are not all trivially zero-output tests. Eq20 padded the different auxiliary/output sum domains into one 3-variable virtual oracle; this is algebraically equivalent for Boolean-sum checking but NOT a byte-identical implementation of paper's precise Eq20 optimizer. Eq17–19 zero transcripts provide extra structural sanity but little independent assurance beyond their exact zero-gate equations.
[INDEPENDENT NOTE] I72 results JSON mistakenly says `degree_d:0` because its script overwrites Python variable `d` in `for d in seq`; this was only JSON metadata. Actual N8 irreducible factor degrees checked correctly using d4 earlier in that script. I73 explicitly pins/report d=4, doesn't change prior evidence files.
[NO CLAIM] No cryptographic commitment keys/opening, no Fiat-Shamir, no complete authors reference implementation, no all-messages-fully-pinned transcript from Appendix E.1 with author's exact vector variable packing. One hypothetical extra verifier constraint not described in the inspected original could change end-to-end exploitability, and the official newest PDF byte authenticity remains VERSION_UNVERIFIED.

## Interpretation and next narrow action
[VERDICT] The strongest additional check in Eq16, y public binding Eq20, and all displayed GKR recurrence/selector identities do NOT forbid the bounded-public-output false rescale instance. This supports an explicit formal ideal-PIOP computation statement soundness counterexample against the inspected revision's intended R_CKKS, contingent on the documented CRT diagonal lookup discrepancy.
[HUMAN REVIEW] Increased confidence warrants a *confidential* author technical query if PI explicitly approves; nothing external sent.
STATUS: PASS (source Eq16–20 algebraic/oracle identities and five local honest sumchecks), UNCLEAR (full exact original protocol serialization and current official PDF bytes).
RESULT: Same fixed public y173, wrem4017060, zero inputs passes extra Eq16 c'−r−py equality and all Eq17–20 source-prescribed GKR wiring. Demonstrated nontrivial honest Eq16/Eq20 sumcheck transcripts plus selector identities with a single consistent Vout and Vaux oracle.
NEXT_ACTION: Build ONE compact <2-page confidential technical note for human PI to approve, fixing manuscript sources and writing the exact stronger Eq16 identity and the full zero-input/nonzero-public-output witness, and request explicit authorization BEFORE contacting paper authors. If PI prefers no contact, the next technical task is replicate source Appendix E.1 step-by-step in its exact variable-packing and verify every final oracle opening under a fixed public-coin challenge schedule, without additional parameter variants.
STATE_UPDATE: NO — parked unrelated RIG-HE STATE.md preserved.
