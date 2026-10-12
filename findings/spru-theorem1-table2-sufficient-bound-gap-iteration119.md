# Iteration 119 — SPRU Theorem 1 vs Table 2: sufficient-bound certification gap

Date: 2026-10-12. PI authorized resumption after I118. ONE hypothesis and ONE decisive source-anchored parameter-substitution test. This is NOT a cryptographic correctness break, benchmark failure, or security attack.

## Sources and provenance
Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, IACR ePrint **2025/651**: https://eprint.iacr.org/2025/651.
Research MCP fetched the full 42-physical-page PDF from fixed GitHub ePrint mirror (source_kind github-mirror), SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, revision `cf9c10e8a26a2b4fcef7a8f22e2a8a33b86ee742`, official latest `VERSION_UNVERIFIED`. Independently inspected the rendered arXiv version at https://arxiv.org/pdf/2607.27401 (physical pp7,14,24,41).
Source anchors: §3.1 physical p7: κ is a **positive integer** for centered binomial noise χκ. §4.1 Theorem 1 p14: Δ ≥ max(4 N² κ q, (20 N³ κ)²). Appendix E proof p41: second sufficient term derives from a loose worst-case product-tree noise bound and Δ ≥ E². §6.1/Table 2 p23–24: New boot. ring N=2^15, rescaling base Δ≈2^49, h=64, optimized depth ℓc=7, reported ~14-bit precision.

## ONE hypothesis and ONE test
[HYPOTHESIS] Theorem 1's **stated sufficient** error/scale conditions directly certify the reported Table 2 New boot. scaling at N=2^15 and Δ≈2^49.

[FALSIFIER] Substitute the reported N and Δ into the *q-independent* necessary portion of the sufficient condition Δ ≥ (20N³κ)², using κ=1 (smallest permitted positive integer). Failure already suffices; no actual encrypted run is claimed.

[DERIVED / TEST RESULT]
```
κ ≥ 1, N=2^15, Δ≈2^49.
(20 N^3 κ)^2 ≥ (20·(2^15)^3)^2 = 400·2^90
                                 = 495176015714152109959649689600
log2 minimum sufficient Δ ≥ 98.64385618977472
log2 Table 2 Δ ≈ 49
minimum gap ≈ 49.643856 bits; factor 400·2^41 = 879609302220800.
Equivalently, Table2 Δ would force κ ≤ sqrt(2^49)/(20·(2^15)^3)
≈ 3.3717478808715225e−8, impossible for positive integer κ.
```

[NEGATIVE] **FAIL** the hypothesis of direct Theorem-1 certification for Table 2. The bound is sufficient rather than necessary, so failure to satisfy it does not disprove correctness, noise safety, or measured ~14-bit precision.

## Critical scope separation
[FACT] Theorem 1 covers the *unoptimized* §4.1 Eq. (8) with a depth-log₂N product tree. Table 2 concerns a *different optimized sparse-block/packed* algorithm with product depth log₂h+1 and other trace/SlotToCoeff steps. Therefore the calculation cannot establish a flaw in the implemented circuit, does not establish that authors asserted Theorem 1 certifies the concrete setup, and cannot be extrapolated into a compiled CKKS failure.
[OPEN] Does a **rigorous tighter circuit-specific noise theorem** prove correctness at the exact Table 2 parameters with negligible failure? This would require a distinct proof/implementation review. None was performed. Existing loose FHE bounds commonly overestimate noise; no new cryptographic contribution is demonstrated. NOVELTY NOT VERIFIED.

## Iteration closure
STATUS: FAIL direct-certification hypothesis; PASS reproducible parameter-substitution check; HUMAN_REVIEW on pursuing a tight bound.
RESULT: Theorem 1's published sufficient Δ lower bound is at least ~2^98.64 when N=2^15 versus Table 2's Δ≈2^49; this is a **formal certificate coverage mismatch**, NOT an algorithmic defect.
NEXT_ACTION: PI must decide whether to authorize a **new, separately defined** I120 hypothesis about a tight proof for the actual optimized sparse-block SPRU circuit, or PARK this proof-bound audit and select a different structural FHE target. Do not automatically pursue nearby paper microaudits.
STATE_UPDATE: YES. No author outreach, public disclosure, issues, or PRs.
