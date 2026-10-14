# HERDS H-HERDS-02 — Fixed gadget length does not imply divergent normalized blind-rotation noise



Date: 2026-10-14 Asia/Tokyo. Independent HERDS source audit, after findings/herds-2025-1804-modraise-trace-residual-cancellation-gate.md. Human PI said continue. Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (concurrent vFHE V23 READ ONLY) and preceding HERDS finding. SHIP I226 READ ONLY. No active global/subtrack counters changed.



## Primary source and provenance [FACT]



Binwu Xiang et al., HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping, EUROCRYPT 2026, ePrint 2025/1804, https://eprint.iacr.org/2025/1804 , publisher DOI https://doi.org/10.1007/978-3-032-25327-9_8. Original complete 46pp Research MCP full PDF via fixed mirror https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/1804.pdf ; SHA256 c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7; VERSION_UNVERIFIED vs official final. Inspected pp9–10 §2.2 gadget requiring B^d|q and epsilon=q/B^d, physical p16 Lemma5 two-term blind rotation variance formula, p21 Theorem1 unit gadget-product cost O(kn) and 6sigma<q/16 criterion, and p26–27 Table3 component-specific concrete lengths and bases. PDF text math glyphs not visually verified against final publisher edition, so do not allege defects based on transcription. Table3 actually changes BRK d_br from 3 to 4 across k2–32; trace and hybrid parameters have distinct d_tr and d_r. The packed-RLEV length d is not interchangeable with all these.



## ONE primary hypothesis and cheapest decisive falsification



H-HERDS-02: Under q=Theta(k n^2), the original Lemma5 upper bound NECESSARILY fails to make sigma_br/q small if d_br is kept as the fixed constant 2, for EVERY possible admissible growing gadget base B_br. Therefore Theorem1 has an intrinsic contradiction even before the other bootstrapping components.



Test: Construct one source-valid unbounded parameter family with fixed d_br=2, integer power-of-two base B whose square divides q, and relative Lemma5 RHS tending to zero. Do not infer correctness of Lemmas6–7 or 128-bit security.



## Analytical result [DERIVATION]



Source Lemma5: sigma_br^2 <= d_br*n*N*B_br^2*sigma_brk^2/3 + (2*n*(N+1)/(3*ell))*(q/B_br^d_br)^2.

Divide by q^2; write F(B)=A*B^2/q^2+C/B^(2*d_br), with A=d_br*n*N*sigma_brk^2/3 and C=2*n*(N+1)/(3*ell). For a positive real base the balancing derivative gives B^(2*(d_br+1))=d_br*C*q^2/A = 2*(N+1)*q^2/(ell*N*sigma_brk^2). For N=Theta(n), fixed coefficient-unit sigma_brk and q=Theta(n^2), optimal B=Theta(n^(2/(d_br+1))). This is a bound minimizer, not a security/precision/implementation optimization proof.



Explicit integral counterfamily: k=2 constant, n=N=2^t, q=2^(2t)=n^2, ell=2, d_br=2, sigma_brk=1 absolute coefficient unit, B_br=2^floor(2t/3). Then B_br^2 divides q exactly, satisfying source digit-gadget condition. Both terms in F(B) have scaling Theta(n^(-2/3)); hence sigma_br/q=O(n^(-1/3)) tends to zero without increasing d_br. H-HERDS-02 FAILS at the precise limited Lemma5 source-noise level.



By contrast if B_br is held constant at 256 while n,N grow, the source's *upper-bound formula* contributes C/B^4=Theta(n*N) to relative variance and therefore stops certifying correctness. Growth of a variance UPPER BOUND does NOT prove real algorithm error, a security failure, or an impossibility theorem. Constant gadget length and constant gadget base are different claims.



## One exact computation [COMPUTED]



Computed with Python Fraction (no floating-point approximation for bound); Decimal only for display. Verified all B_br^2|q.

t=12: n=2^12, B=2^8, 6*sqrt(F)=0.3750152585 (fails isolated 1/16 diagnostic).

t=18: n=2^18, B=2^12, ratio=0.0937500596 (fails).

t=21: n=2^21, B=2^14, ratio=0.0468750037 (passes isolated 1/16 diagnostic).

t=24: n=2^24, B=2^16, ratio=0.0234375002 (passes).

t=30: n=2^30, B=2^20, ratio=0.0058593750 (passes).

Fixed B=256 instead gives ratios 0.3750152585 at t12, 13.8564337 at t18, 110.8512781 at t21, 886.8100399 at t24 and 56755.8409 at t30; these are values of an upper bound, NOT actual decryption failures.

Reproducible script /mnt/data/herds_I02_br_gadget_asymptotic_gate.py SHA256 17244ad618858f8e653a7a53acd1e6fef7455563e24a98024197bb2db6a9b595 ; JSON /mnt/data/herds_I02_br_gadget_asymptotic_results.json SHA256 450c8eac85365e6a4c52e61a6ecc1ca07ff2bd4930fff69ee1d9783bbc9b2a71 .



## Honest technical scope and decision



STATUS: FAIL H-HERDS-02 inherent fixed d_br=2 impossibility. PASS explicit integer-divisible conditional family and exact Lemma5 normalized-variance calculation. Overall Theorem1, secure key/noise/parameters, full DFR and concrete bit complexity UNCLEAR. NOVELTY NOT VERIFIED.

RESULT: It is mathematically possible at the isolated blind-rotation noise-bound level to keep gadget length fixed while scaling its base. The paper states the gadget-product unit-cost convention; q-growth also affects bit complexity. A complete bootstrap must account for Lemma6 trace/modswitch/keyswitch noise and Lemma7 hybrid accumulator with separate B_tr,d_tr,B_r,d_r. The toy family assumes coefficient absolute BRK sigma=1 and astronomically large n, unlike reported q2^64 N2048 n560/636 beta values. Passing isolated 6sigma<q/16 does NOT certify the overall source security or decryption correctness.

NEXT_ACTION: PARK the generic fixed-length contradiction suspicion; do not repeat adjacent gadget radix scans. If PI continues HERDS, require a source-matched full Lemma5–7 security/DFR parameter worksheet and runnable source, or select another real FHE technical gap. Levis full text separately source-blocked. No original-paper flaw or cryptanalytic attack shown.

STATE_UPDATE: YES this narrow finding; NO edits to global STATE.md/vFHE, SHIP checkpoint, missing-source backlog, or upstream code.